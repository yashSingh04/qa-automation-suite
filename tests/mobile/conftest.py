"""Appium fixtures.

Kept in its own conftest so the web and API suites never import the Appium
client — `pytest -m api` stays a five-second run with no mobile dependencies.
"""
import os

import pytest

from utils.config import Config


def _android_options():
    from appium.options.android import UiAutomator2Options

    options = UiAutomator2Options()
    options.platform_name = Config.PLATFORM_NAME
    options.automation_name = Config.AUTOMATION_NAME
    options.device_name = Config.DEVICE_NAME
    options.new_command_timeout = Config.NEW_COMMAND_TIMEOUT
    options.auto_grant_permissions = True
    # Faster, more deterministic resets between tests.
    options.set_capability("appium:disableWindowAnimation", True)

    if Config.PLATFORM_VERSION:
        options.platform_version = Config.PLATFORM_VERSION

    app_path = os.path.abspath(Config.APP_PATH)
    if os.path.exists(app_path):
        options.app = app_path
    else:
        # App already installed on the device — launch by package/activity.
        options.app_package = Config.APP_PACKAGE
        options.app_activity = Config.APP_ACTIVITY
    return options


@pytest.fixture(scope="function")
def appium_driver():
    """One session per test, so app state never leaks between cases."""
    from appium import webdriver

    driver = webdriver.Remote(Config.APPIUM_SERVER, options=_android_options())
    yield driver
    driver.quit()


@pytest.fixture
def home_screen(appium_driver):
    from mobile.pages.api_demos_home import ApiDemosHome

    page = ApiDemosHome(appium_driver)
    assert page.is_loaded(), "Precondition failed: ApiDemos home screen did not load"
    return page

"""Shared fixtures: WebDriver lifecycle, API client, screenshot-on-failure."""
import logging
import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from utils.api_client import APIClient
from utils.config import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

SCREENSHOT_DIR = "screenshots"


def _chrome_options() -> ChromeOptions:
    opts = ChromeOptions()
    if Config.HEADLESS:
        opts.add_argument("--headless=new")
    opts.add_argument(f"--window-size={Config.WINDOW_SIZE}")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    # Suppress the Chrome password-manager / leak-detection popups that
    # otherwise intercept clicks on login forms.
    opts.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    opts.add_argument("--disable-search-engine-choice-screen")
    return opts


def _firefox_options() -> FirefoxOptions:
    opts = FirefoxOptions()
    if Config.HEADLESS:
        opts.add_argument("-headless")
    return opts


@pytest.fixture(scope="function")
def driver():
    """Fresh browser per test — no state bleeding between cases.

    Selenium Manager (4.6+) resolves the driver binary automatically,
    so there is no webdriver-manager dependency and nothing to pin in CI.
    """
    browser = Config.BROWSER.lower()
    if browser == "chrome":
        drv = webdriver.Chrome(options=_chrome_options())
    elif browser == "firefox":
        drv = webdriver.Firefox(options=_firefox_options())
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    drv.implicitly_wait(Config.IMPLICIT_WAIT)
    yield drv
    drv.quit()


@pytest.fixture(scope="session")
def api():
    client = APIClient()
    yield client
    client.close()


@pytest.fixture
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver).load()


@pytest.fixture
def inventory_page(login_page):
    """Authenticated session as the standard user."""
    page = login_page.login(Config.STANDARD_USER, Config.PASSWORD)
    assert page.is_loaded(), "Precondition failed: could not reach inventory page"
    return page


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to any failed UI test."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv:
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            path = os.path.join(SCREENSHOT_DIR, f"{item.name}_{stamp}.png")
            try:
                drv.save_screenshot(path)
                print(f"\n[screenshot] {path}")
            except Exception as exc:  # pragma: no cover
                print(f"\n[screenshot failed] {exc}")

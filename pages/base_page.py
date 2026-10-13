"""BasePage: every page object inherits these interaction primitives.

All waits are explicit. No time.sleep() anywhere in this suite.
"""
import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import Config

log = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)

    # --- navigation ---
    def open(self, path: str = ""):
        url = f"{Config.BASE_URL}{path}"
        log.info("Navigating to %s", url)
        self.driver.get(url)
        return self

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    # --- element access ---
    def find(self, locator):
        """Wait for presence, then return the element."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text: str):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def text_of(self, locator) -> str:
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    # --- state queries ---
    def is_visible(self, locator, timeout: int = None) -> bool:
        """Non-throwing visibility check — used for assertions, not control flow."""
        try:
            WebDriverWait(self.driver, timeout or Config.EXPLICIT_WAIT).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, fragment: str) -> bool:
        try:
            return self.wait.until(EC.url_contains(fragment))
        except TimeoutException:
            return False

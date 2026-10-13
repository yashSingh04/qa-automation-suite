"""BaseMobilePage: interaction primitives for Appium page objects.

Mirrors the structure of pages/base_page.py so the web and mobile suites
read the same way. All waits are explicit; gestures use the UiAutomator2
`mobile:` commands rather than deprecated TouchAction.
"""
import logging

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import Config

log = logging.getLogger(__name__)


class BaseMobilePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.APPIUM_EXPLICIT_WAIT)

    # --- element access ---
    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def tap(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text: str):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def text_of(self, locator) -> str:
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def is_visible(self, locator, timeout: int = None) -> bool:
        """Non-throwing visibility check, for assertions rather than control flow."""
        try:
            WebDriverWait(self.driver, timeout or Config.APPIUM_EXPLICIT_WAIT).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # --- gestures (UiAutomator2 mobile: commands) ---
    def swipe(self, direction: str = "up", percent: float = 0.75):
        """Swipe within the current window bounds."""
        size = self.driver.get_window_size()
        self.driver.execute_script("mobile: swipeGesture", {
            "left": 0, "top": 0, "width": size["width"], "height": size["height"],
            "direction": direction,
            "percent": percent,
        })

    def scroll_to_text(self, text: str):
        """Scroll a scrollable container until `text` is on screen.

        Uses UiScrollable, which handles the scrolling loop natively and is
        far more reliable than repeatedly swiping and re-checking.
        """
        selector = (
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().textContains("{text}"))'
        )
        return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector)

    def long_press(self, locator, duration_ms: int = 1500):
        element = self.find(locator)
        self.driver.execute_script("mobile: longClickGesture", {
            "elementId": element.id,
            "duration": duration_ms,
        })

    def drag_and_drop(self, source_locator, target_locator):
        source = self.find(source_locator)
        target = self.find(target_locator)
        end = target.location
        self.driver.execute_script("mobile: dragGesture", {
            "elementId": source.id,
            "endX": end["x"],
            "endY": end["y"],
        })

    # --- device / app state ---
    def back(self):
        self.driver.back()
        return self

    def hide_keyboard(self):
        try:
            self.driver.hide_keyboard()
        except Exception:  # keyboard already hidden
            pass
        return self

    @property
    def current_activity(self) -> str:
        return self.driver.current_activity

    def rotate(self, orientation: str = "LANDSCAPE"):
        self.driver.orientation = orientation
        return self

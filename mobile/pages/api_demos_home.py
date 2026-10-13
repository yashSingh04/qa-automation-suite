"""Page objects for the ApiDemos sample app.

ApiDemos is the canonical Appium practice application (the one shipped with
Appium's own test suite), so its screens are stable across versions and it is
freely downloadable. The top-level screen is a list of category rows.
"""
from appium.webdriver.common.appiumby import AppiumBy

from mobile.pages.base_mobile_page import BaseMobilePage


class ApiDemosHome(BaseMobilePage):
    """Top-level category list: Accessibility, Animation, App, Content, ..."""

    LIST = (AppiumBy.ID, "android:id/list")
    ROWS = (AppiumBy.ID, "android:id/text1")

    # Accessibility IDs on this screen are the visible row labels.
    ACCESSIBILITY = (AppiumBy.ACCESSIBILITY_ID, "Accessibility")
    ANIMATION = (AppiumBy.ACCESSIBILITY_ID, "Animation")
    APP = (AppiumBy.ACCESSIBILITY_ID, "App")
    CONTENT = (AppiumBy.ACCESSIBILITY_ID, "Content")
    GRAPHICS = (AppiumBy.ACCESSIBILITY_ID, "Graphics")
    MEDIA = (AppiumBy.ACCESSIBILITY_ID, "Media")
    PREFERENCE = (AppiumBy.ACCESSIBILITY_ID, "Preference")
    TEXT = (AppiumBy.ACCESSIBILITY_ID, "Text")
    VIEWS = (AppiumBy.ACCESSIBILITY_ID, "Views")

    EXPECTED_CATEGORIES = [
        "Accessibility", "Animation", "App", "Content",
        "Graphics", "Media", "NFC", "OS", "Preference", "Text", "Views",
    ]

    def is_loaded(self) -> bool:
        return self.is_visible(self.LIST)

    def category_labels(self) -> list:
        return [row.text for row in self.find_all(self.ROWS)]

    def open_category(self, name: str):
        """Scroll the category into view if needed, then open it."""
        self.scroll_to_text(name).click()
        return CategoryScreen(self.driver)

    def open_views(self):
        self.tap(self.VIEWS)
        return CategoryScreen(self.driver)


class CategoryScreen(BaseMobilePage):
    """Any second-level list screen reached from the home categories."""

    LIST = (AppiumBy.ID, "android:id/list")
    ROWS = (AppiumBy.ID, "android:id/text1")

    def is_loaded(self) -> bool:
        return self.is_visible(self.LIST)

    def item_labels(self) -> list:
        return [row.text for row in self.find_all(self.ROWS)]

    def open_item(self, name: str):
        self.scroll_to_text(name).click()
        return self

    def has_item(self, name: str) -> bool:
        return name in self.item_labels()


class TextFieldsScreen(BaseMobilePage):
    """Views > Controls > Light Theme — simple input controls."""

    EDIT_TEXT = (AppiumBy.CLASS_NAME, "android.widget.EditText")
    CHECKBOX = (AppiumBy.CLASS_NAME, "android.widget.CheckBox")
    BUTTON = (AppiumBy.CLASS_NAME, "android.widget.Button")

    def enter_text(self, text: str):
        self.type(self.EDIT_TEXT, text)
        return self

    def entered_text(self) -> str:
        return self.find(self.EDIT_TEXT).text

    def toggle_checkbox(self):
        self.tap(self.CHECKBOX)
        return self

    def checkbox_is_checked(self) -> bool:
        return self.find(self.CHECKBOX).get_attribute("checked") == "true"

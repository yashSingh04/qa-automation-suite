from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "h3[data-test='error']")
    LOGO = (By.CLASS_NAME, "login_logo")

    def load(self):
        return self.open("/")

    def login(self, username: str, password: str):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)
        return InventoryPage(self.driver)

    @property
    def error_message(self) -> str:
        return self.text_of(self.ERROR)

    def has_error(self) -> bool:
        return self.is_visible(self.ERROR, timeout=5)

    def is_loaded(self) -> bool:
        return self.is_visible(self.LOGO)

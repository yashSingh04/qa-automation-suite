from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage


class CartPage(BasePage):
    ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def is_loaded(self) -> bool:
        return self.wait_for_url_contains("cart.html")

    def item_count(self) -> int:
        return len(self.driver.find_elements(*self.ITEMS))

    def item_names(self) -> list:
        return [e.text for e in self.driver.find_elements(*self.ITEM_NAMES)]

    def checkout(self):
        self.click(self.CHECKOUT)
        return CheckoutPage(self.driver)

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.cart_page import CartPage


class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SORT = (By.CLASS_NAME, "product_sort_container")

    def is_loaded(self) -> bool:
        return self.wait_for_url_contains("inventory.html")

    @property
    def title(self) -> str:
        return self.text_of(self.TITLE)

    def item_count(self) -> int:
        return len(self.find_all(self.ITEMS))

    def product_names(self) -> list:
        return [e.text for e in self.find_all(self.ITEM_NAMES)]

    def prices(self) -> list:
        return [float(e.text.replace("$", "")) for e in self.find_all(self.ITEM_PRICES)]

    def add_to_cart(self, product_name: str):
        slug = product_name.lower().replace(" ", "-")
        self.click((By.ID, f"add-to-cart-{slug}"))
        return self

    def remove_from_cart(self, product_name: str):
        slug = product_name.lower().replace(" ", "-")
        self.click((By.ID, f"remove-{slug}"))
        return self

    def cart_count(self) -> int:
        if not self.is_visible(self.CART_BADGE, timeout=3):
            return 0
        return int(self.text_of(self.CART_BADGE))

    def sort_by(self, option_value: str):
        from selenium.webdriver.support.ui import Select
        Select(self.find(self.SORT)).select_by_value(option_value)
        return self

    def go_to_cart(self):
        self.click(self.CART_LINK)
        return CartPage(self.driver)

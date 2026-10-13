from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    FINISH = (By.ID, "finish")
    ERROR = (By.CSS_SELECTOR, "h3[data-test='error']")
    SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX = (By.CLASS_NAME, "summary_tax_label")
    TOTAL = (By.CLASS_NAME, "summary_total_label")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def fill_details(self, first: str, last: str, postcode: str):
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, postcode)
        self.click(self.CONTINUE)
        return self

    def has_error(self) -> bool:
        return self.is_visible(self.ERROR, timeout=5)

    @property
    def error_message(self) -> str:
        return self.text_of(self.ERROR)

    def _money(self, locator) -> float:
        return float(self.text_of(locator).split("$")[1])

    @property
    def subtotal(self) -> float:
        return self._money(self.SUBTOTAL)

    @property
    def tax(self) -> float:
        return self._money(self.TAX)

    @property
    def total(self) -> float:
        return self._money(self.TOTAL)

    def finish(self):
        self.click(self.FINISH)
        return self

    def is_order_complete(self) -> bool:
        return self.is_visible(self.COMPLETE_HEADER)

    @property
    def confirmation_text(self) -> str:
        return self.text_of(self.COMPLETE_HEADER)

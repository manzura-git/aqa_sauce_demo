from playwright.sync_api import expect

from pages.base_page import BasePage


class CartPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.cart_item_name = self.page.locator(".inventory_item_name")
        self.cart_item_price = self.page.locator(".inventory_item_price")
        self.btn_remove = self.page.locator("[data-test='remove-sauce-labs-backpack']")
        self.btn_checkout = self.page.get_by_role("button", name="Checkout")
        self.btn_continue_shopping = self.page.get_by_role("button", name="Continue Shopping")
        self.cart_badge = self.page.locator(".shopping_cart_badge")
        self.cart_items = self.page.locator(".cart_item")

    def check_item_visible(self):
        expect(self.cart_item_name).to_be_visible()

    def check_item_name(self, name: str):
        expect(self.cart_item_name).to_have_text(name)

    def check_item_price(self, price: str):
        expect(self.cart_item_price).to_have_text(price)

    def click_checkout(self):
        self.btn_checkout.click()

    def click_remove(self):
        self.btn_remove.click()

    def click_continue_shopping(self):
        self.btn_continue_shopping.click()

    def check_cart_is_empty(self):
        expect(self.cart_item_name).not_to_be_visible()

    def check_cart_badge_not_visible(self):
        expect(self.cart_badge).not_to_be_visible()

    def get_items_count(self) -> int:
        return self.cart_items.count()

    def check_items_count(self, count: int):
        assert self.cart_items.count() == count,\
            f"Ожидалось {count} товаров, найдено {self.cart_items.count()}"

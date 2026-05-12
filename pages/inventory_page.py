from playwright.sync_api import expect

from config.products import BACKPACK
from pages.base_page import BasePage


class InventoryPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.title = self.page.locator(".title")
        self.backpack1 = self.page.get_by_text(BACKPACK)
        self.price = self.page.locator(f"//*[text()='{BACKPACK}']/../../..//*[@class='inventory_item_price']")
        self.btn_add_to_card = self.page.locator(f"//*[text()='{BACKPACK}']/../../..//button")
        self.loc_price = "../../*[@class='inventory_item_price']"
        self.cart_badge = self.page.locator(".shopping_cart_badge")
        self.sort_select = self.page.locator("select.product_sort_container")
        self.btn_remove_backpack = self.page.locator("[data-test='remove-sauce-labs-backpack']")

    def check_backpack1_visible(self):
        expect(self.backpack1).to_be_visible()

    def get_backpack1_price(self) -> str:
        return self.price.text_content()

    def check_is_price(self):
        assert self.get_backpack1_price().startswith("$")

    def click_btn_add_to_cart(self):
        self.btn_add_to_card.click()

    def click_add_to_cart_by_name(self, product_name: str):
        self.page.locator(f".inventory_item:has-text('{product_name}') button").click()

    def check_cart_badge(self, count: str):
        expect(self.cart_badge).to_have_text(count)

    def check_cart_badge_not_visible(self):
        expect(self.cart_badge).not_to_be_visible()

    def have_title(self, title_text: str):
        expect(self.title).to_be_visible()
        expect(self.title).to_have_text(title_text)
        return True

    def get_item_count(self) -> int:
        return self.page.locator(".inventory_item").count()

    def get_all_names(self) -> list:
        return self.page.locator(".inventory_item_name").all_text_contents()

    def get_all_prices(self) -> list:
        texts = self.page.locator(".inventory_item_price").all_text_contents()
        return [float(t.replace("$", "")) for t in texts]

    def select_sort(self, value: str):
        self.sort_select.select_option(value)

    def click_remove_backpack(self):
        self.btn_remove_backpack.click()

    def check_remove_btn_visible(self):
        expect(self.btn_remove_backpack).to_be_visible()

    def check_images_loaded(self):
        self.page.wait_for_function(
            "() => Array.from(document.querySelectorAll('.inventory_item img'))"
            ".every(img => img.complete && img.naturalWidth > 0)"
        )

    def click_cart_icon(self):
        self.page.locator(".shopping_cart_link").click()

    def click_backpack_image(self):
        self.page.locator(
            f"//*[text()='{BACKPACK}']/ancestor::div[contains(@class,'inventory_item')]//img"
        ).click()

    def click_logo(self):
        self.page.locator(".app_logo").click()

    def open_hamburger_menu(self):
        self.page.locator("#react-burger-menu-btn").click()

    def close_hamburger_menu(self):
        self.page.locator("#react-burger-cross-btn").click()

    def logout(self):
        self.page.locator("#react-burger-menu-btn").click()
        self.page.locator("#logout_sidebar_link").click()

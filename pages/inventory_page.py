import re

import allure
from playwright.sync_api import expect

from config.products import BACKPACK
from pages.base_page import BasePage

_JS_BROKEN_IMGS = (
    "() => Array.from("
    "document.querySelectorAll('.inventory_item img')"
    ").filter(img => !img.complete || img.naturalWidth === 0)"
    ".length"
)

_JS_ALL_IMGS_LOADED = (
    "() => Array.from("
    "document.querySelectorAll('.inventory_item img')"
    ").every(img => img.complete && img.naturalWidth > 0)"
)


class InventoryPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.title = self.page.locator(".title")
        self.backpack1 = self.page.get_by_text(BACKPACK)
        self.price = self.page.locator(
            f"//*[text()='{BACKPACK}']"
            f"/../../..//*[@class='inventory_item_price']"
        )
        self.btn_add_to_card = self.page.locator(
            f"//*[text()='{BACKPACK}']/../../..//button"
        )
        self.cart_badge = self.page.locator(".shopping_cart_badge")
        self.sort_select = self.page.locator(
            "select.product_sort_container"
        )
        self.btn_remove_backpack = self.page.locator(
            "[data-test='remove-sauce-labs-backpack']"
        )
        self.inventory_items = self.page.locator(".inventory_item")
        self.inventory_item_names = self.page.locator(
            ".inventory_item_name"
        )
        self.inventory_item_prices = self.page.locator(
            ".inventory_item_price"
        )
        self.inventory_images = self.page.locator(".inventory_item img")
        self.cart_icon = self.page.locator(".shopping_cart_link")
        self.backpack_image = self.page.locator(
            f"//*[text()='{BACKPACK}']"
            f"/ancestor::div[contains(@class,'inventory_item')]//img"
        )
        self.logo = self.page.locator(".app_logo")
        self.hamburger_menu_btn = self.page.locator(
            "#react-burger-menu-btn"
        )
        self.hamburger_close_btn = self.page.locator(
            "#react-burger-cross-btn"
        )
        self.logout_link = self.page.locator("#logout_sidebar_link")
        self.sidebar_inventory_link = self.page.locator(
            "#inventory_sidebar_link"
        )
        self.sidebar_about_link = self.page.locator(
            "#about_sidebar_link"
        )
        self.sidebar_reset_link = self.page.locator(
            "#reset_sidebar_link"
        )
        self.add_to_cart_selector = (
            ".inventory_item:has-text('{}') button"
        )

    # --- товары ---

    def check_backpack1_visible(self):
        expect(self.backpack1).to_be_visible()

    def get_backpack1_price(self) -> str:
        return self.price.text_content()

    def check_is_price(self):
        assert self.get_backpack1_price().startswith("$")

    @allure.step("Добавить рюкзак в корзину")
    def click_btn_add_to_cart(self):
        self.btn_add_to_card.click()

    @allure.step("Добавить товар '{product_name}' в корзину")
    def click_add_to_cart_by_name(self, product_name: str):
        self.page.locator(
            self.add_to_cart_selector.format(product_name)
        ).click()

    @allure.step("Проверить видимость кнопки Remove")
    def check_remove_btn_visible(self):
        expect(self.btn_remove_backpack).to_be_visible()

    @allure.step("Удалить рюкзак из корзины")
    def click_remove_backpack(self):
        self.btn_remove_backpack.click()

    def get_item_count(self) -> int:
        return self.inventory_items.count()

    def get_all_names(self) -> list:
        return self.inventory_item_names.all_text_contents()

    def get_all_prices_text(self) -> list:
        """Возвращает цены как строки, например ['$29.99', '$9.99']."""
        return self.inventory_item_prices.all_text_contents()

    def get_all_prices(self) -> list:
        """Возвращает цены как float для сортировки."""
        return [
            float(t.replace("$", ""))
            for t in self.get_all_prices_text()
        ]

    # --- изображения ---

    @allure.step("Проверить загрузку всех изображений")
    def check_images_loaded(self):
        self.page.wait_for_function(_JS_ALL_IMGS_LOADED)

    def get_broken_images_count(self) -> int:
        return self.page.evaluate(_JS_BROKEN_IMGS)

    @allure.step("Проверить alt-атрибуты у всех изображений")
    def check_all_images_have_alt(self):
        for img in self.inventory_images.all():
            alt = img.get_attribute("alt")
            assert alt is not None and alt != "", (
                "Изображение без alt-атрибута"
            )

    # --- корзина ---

    @allure.step("Проверить счётчик корзины: {count}")
    def check_cart_badge(self, count: str):
        expect(self.cart_badge).to_have_text(count)

    @allure.step("Проверить, что счётчик корзины скрыт")
    def check_cart_badge_not_visible(self):
        expect(self.cart_badge).not_to_be_visible()

    @allure.step("Перейти в корзину")
    def click_cart_icon(self):
        self.cart_icon.click()

    # --- сортировка ---

    @allure.step("Выбрать сортировку: {value}")
    def select_sort(self, value: str):
        self.sort_select.select_option(value)

    # --- навигация ---

    @allure.step("Проверить заголовок страницы: {title_text}")
    def have_title(self, title_text: str):
        expect(self.title).to_be_visible()
        expect(self.title).to_have_text(title_text)
        return True

    @allure.step("Кликнуть по изображению рюкзака")
    def click_backpack_image(self):
        self.backpack_image.click()

    @allure.step("Кликнуть по логотипу")
    def click_logo(self):
        self.logo.click()

    # --- гамбургер-меню ---

    @allure.step("Открыть гамбургер-меню")
    def open_hamburger_menu(self):
        self.hamburger_menu_btn.click()

    @allure.step("Закрыть гамбургер-меню")
    def close_hamburger_menu(self):
        self.hamburger_close_btn.click()

    @allure.step("Проверить видимость кнопки меню")
    def check_hamburger_btn_visible(self):
        expect(self.hamburger_menu_btn).to_be_visible()

    @allure.step("Проверить видимость ссылок в сайдбаре")
    def check_sidebar_links_visible(self):
        expect(self.sidebar_inventory_link).to_be_visible()
        expect(self.sidebar_about_link).to_be_visible()
        expect(self.logout_link).to_be_visible()
        expect(self.sidebar_reset_link).to_be_visible()

    @allure.step("Проверить скрытость ссылок сайдбара")
    def check_sidebar_links_hidden(self):
        expect(self.sidebar_inventory_link).not_to_be_visible()

    @allure.step("Сбросить состояние приложения")
    def click_reset_app_state(self):
        self.sidebar_reset_link.click()

    @allure.step("Выйти из аккаунта")
    def logout(self):
        self.hamburger_menu_btn.click()
        self.logout_link.click()

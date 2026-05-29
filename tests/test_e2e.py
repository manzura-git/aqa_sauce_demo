"""E2E-тесты: полные пользовательские сценарии."""
import allure
import pytest

from config.base import (
    URL_BASE,
    URL_BASE_ROOT,
    URL_CART_HTML,
    URL_CHECKOUT_STEP1,
    URL_CHECKOUT_STEP2,
    URL_CHECKOUT_COMPLETE,
    URL_INVENTORY,
)
from config.products import BACKPACK, BIKE_LIGHT, BOLT_TSHIRT
from config.users import USER1_NAME, USERS_PASSWORD
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.complete_page import CompletePage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.assertions import assert_total_equals_subtotal_plus_tax


@allure.epic("SauceDemo")
@allure.feature("E2E: Полный цикл покупки")
@pytest.mark.e2e
@pytest.mark.smoke
class TestE2E:

    def _login(self, page):
        login = LoginPage(page)
        login.open()
        login.fill_username(USER1_NAME)
        login.fill_password(USERS_PASSWORD)
        login.click_btn_login()
        login.expect_to_have_url("/inventory.html")
        return page

    @allure.story("TC_CHECK_001")
    @allure.title("Полный цикл покупки одного товара")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.high
    def test_e2e_full_checkout_single_item(self, page):
        """TC_CHECK_001: полный цикл покупки одного товара."""
        self._login(page)

        inventory = InventoryPage(page)
        assert inventory.have_title("Products")
        inventory.click_btn_add_to_cart()
        inventory.check_cart_badge("1")

        inventory.click_cart_icon()
        cart = CartPage(page)
        cart.check_item_visible()
        cart.check_item_name(BACKPACK)
        cart.check_items_count(1)

        cart.click_checkout()
        checkout = CheckoutPage(page)
        checkout.expect_to_have_url(URL_CHECKOUT_STEP1)
        checkout.fill_info("Иван", "Иванов", "12345")
        checkout.click_continue()
        checkout.expect_to_have_url(URL_CHECKOUT_STEP2)

        item_total = checkout.get_item_total()
        tax = checkout.get_tax()
        total = checkout.get_total()
        assert_total_equals_subtotal_plus_tax(item_total, tax, total)

        checkout.click_finish()
        checkout.expect_to_have_url(URL_CHECKOUT_COMPLETE)
        complete = CompletePage(page)
        assert complete.check_order_complete()

    @allure.story("TC_CHECK_010")
    @allure.title("Полный цикл покупки нескольких товаров")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_e2e_full_checkout_multiple_items(self, page):
        """TC_CHECK_010: полный цикл покупки нескольких товаров."""
        self._login(page)

        inventory = InventoryPage(page)
        inventory.click_add_to_cart_by_name(BACKPACK)
        inventory.click_add_to_cart_by_name(BIKE_LIGHT)
        inventory.click_add_to_cart_by_name(BOLT_TSHIRT)
        inventory.check_cart_badge("3")

        inventory.click_cart_icon()
        cart = CartPage(page)
        cart.check_items_count(3)

        cart.click_checkout()
        checkout = CheckoutPage(page)
        checkout.fill_info("Анна", "Смирнова", "67890")
        checkout.click_continue()
        checkout.expect_to_have_url(URL_CHECKOUT_STEP2)

        item_total = checkout.get_item_total()
        tax = checkout.get_tax()
        total = checkout.get_total()
        assert_total_equals_subtotal_plus_tax(item_total, tax, total)

        checkout.click_finish()
        complete = CompletePage(page)
        assert complete.check_order_complete()

    @allure.story("E2E: Добавить-Удалить-Оформить")
    @allure.title("Добавить → удалить → добавить снова → оформить заказ")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_e2e_add_remove_then_checkout(self, page):
        """Добавить товар → удалить → добавить снова → оформить заказ."""
        self._login(page)

        inventory = InventoryPage(page)
        inventory.click_btn_add_to_cart()
        inventory.check_cart_badge("1")
        inventory.click_remove_backpack()
        inventory.check_cart_badge_not_visible()
        inventory.click_btn_add_to_cart()
        inventory.check_cart_badge("1")

        inventory.click_cart_icon()
        cart = CartPage(page)
        cart.check_items_count(1)
        cart.click_checkout()

        checkout = CheckoutPage(page)
        checkout.fill_info("Тест", "Тестов", "00000")
        checkout.click_continue()
        checkout.click_finish()
        assert CompletePage(page).check_order_complete()

    @allure.story("E2E: Back Home")
    @allure.title("После заказа — Back Home возвращает на инвентарь")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_e2e_back_home_after_order(self, page):
        """После заказа — 'Back Home' возвращает на инвентарь."""
        self._login(page)

        inventory = InventoryPage(page)
        inventory.click_btn_add_to_cart()
        inventory.click_cart_icon()
        CartPage(page).click_checkout()

        checkout = CheckoutPage(page)
        checkout.fill_info("А", "Б", "123")
        checkout.click_continue()
        checkout.click_finish()

        complete = CompletePage(page)
        complete.check_order_complete()
        complete.click_back_home()
        complete.expect_to_have_url(URL_INVENTORY)

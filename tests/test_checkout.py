import allure
import pytest

from config.base import (
    URL_BASE,
    URL_CART_HTML,
    URL_CHECKOUT_STEP1,
    URL_CHECKOUT_STEP2,
    E_MSG_CHECKOUT_FIRSTNAME,
    E_MSG_CHECKOUT_LASTNAME,
    E_MSG_CHECKOUT_ZIPCODE,
)
from config.products import BACKPACK, BOLT_TSHIRT
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from utils.assertions import assert_total_equals_subtotal_plus_tax


@allure.epic("SauceDemo")
@allure.feature("Оформление заказа")
@pytest.mark.checkout
class TestCheckoutValidation:

    def _go_to_step1(self, page) -> CheckoutPage:
        inventory = InventoryPage(page)
        inventory.click_btn_add_to_cart()
        page.goto(URL_BASE + URL_CART_HTML)
        CartPage(page).click_checkout()
        checkout = CheckoutPage(page)
        checkout.expect_to_have_url(URL_CHECKOUT_STEP1)
        return checkout

    @allure.story("TC_CHECK_002")
    @allure.title("Пустое First Name — ошибка валидации")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_check_002(self, logged_in_page):
        checkout = self._go_to_step1(logged_in_page)
        checkout.fill_info("", "Иванов", "12345")
        checkout.click_continue()
        assert checkout.check_error(E_MSG_CHECKOUT_FIRSTNAME), \
            "Должна быть ошибка: First Name is required"

    @allure.story("TC_CHECK_003")
    @allure.title("Пустое Last Name — ошибка валидации")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_check_003(self, logged_in_page):
        checkout = self._go_to_step1(logged_in_page)
        checkout.fill_info("Иван", "", "12345")
        checkout.click_continue()
        assert checkout.check_error(E_MSG_CHECKOUT_LASTNAME), \
            "Должна быть ошибка: Last Name is required"

    @allure.story("TC_CHECK_004")
    @allure.title("Пустой Postal Code — ошибка валидации")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_check_004(self, logged_in_page):
        checkout = self._go_to_step1(logged_in_page)
        checkout.fill_info("Иван", "Иванов", "")
        checkout.click_continue()
        assert checkout.check_error(E_MSG_CHECKOUT_ZIPCODE), \
            "Должна быть ошибка: Postal Code is required"

    @allure.story("TC_CHECK_005")
    @allure.title("Нестандартный Postal Code принимается системой")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_check_005(self, logged_in_page):
        checkout = self._go_to_step1(logged_in_page)
        checkout.fill_info("Иван", "Иванов", "ABC-XYZ")
        checkout.click_continue()
        checkout.expect_to_have_url(URL_CHECKOUT_STEP2)

    @allure.story("TC_CHECK_006")
    @allure.title("Cancel возвращает в корзину")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_check_006(self, logged_in_page):
        checkout = self._go_to_step1(logged_in_page)
        checkout.click_cancel()
        checkout.expect_to_have_url(URL_CART_HTML)

    @allure.story("TC_CHECK_008")
    @allure.title("Итоговая сумма = подытог + налог")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_check_008(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_btn_add_to_cart()
        logged_in_page.goto(URL_BASE + URL_CART_HTML)
        CartPage(logged_in_page).click_checkout()
        checkout = CheckoutPage(logged_in_page)
        checkout.fill_info("Иван", "Иванов", "12345")
        checkout.click_continue()
        assert_total_equals_subtotal_plus_tax(
            checkout.get_item_total(),
            checkout.get_tax(),
            checkout.get_total(),
        )

    @allure.story("TC_CHECK_010")
    @allure.title("Два товара: итог = подытог + налог, заказ оформлен")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_check_010(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_add_to_cart_by_name(BACKPACK)
        inventory.click_add_to_cart_by_name(BOLT_TSHIRT)
        inventory.check_cart_badge("2")
        logged_in_page.goto(URL_BASE + URL_CART_HTML)
        cart = CartPage(logged_in_page)
        cart.check_items_count(2)
        cart.click_checkout()
        checkout = CheckoutPage(logged_in_page)
        checkout.fill_info("Иван", "Иванов", "12345")
        checkout.click_continue()
        assert_total_equals_subtotal_plus_tax(
            checkout.get_item_total(),
            checkout.get_tax(),
            checkout.get_total(),
        )
        checkout.click_finish()
        assert checkout.check_order_complete()

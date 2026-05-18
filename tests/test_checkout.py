from config.base import (URL_BASE, URL_CART_HTML, URL_CHECKOUT_STEP1, URL_CHECKOUT_STEP2,
                          E_MSG_CHECKOUT_FIRSTNAME, E_MSG_CHECKOUT_LASTNAME, E_MSG_CHECKOUT_ZIPCODE)
from config.products import BACKPACK, BOLT_TSHIRT
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage


class TestCheckoutValidation:

    def _go_to_step1(self, page) -> CheckoutPage:
        inventory = InventoryPage(page)
        inventory.click_btn_add_to_cart()
        page.goto(URL_BASE + URL_CART_HTML)
        CartPage(page).click_checkout()
        checkout = CheckoutPage(page)
        checkout.expect_to_have_url(URL_CHECKOUT_STEP1)
        return checkout

    def test_check_002(self, logged_in_page):
        checkout = self._go_to_step1(logged_in_page)
        checkout.fill_info("", "Иванов", "12345")
        checkout.click_continue()
        assert checkout.check_error(E_MSG_CHECKOUT_FIRSTNAME), "Должна быть ошибка: First Name is required"

    def test_check_003(self, logged_in_page):
        checkout = self._go_to_step1(logged_in_page)
        checkout.fill_info("Иван", "", "12345")
        checkout.click_continue()
        assert checkout.check_error(E_MSG_CHECKOUT_LASTNAME), "Должна быть ошибка: Last Name is required"

    def test_check_004(self, logged_in_page):
        checkout = self._go_to_step1(logged_in_page)
        checkout.fill_info("Иван", "Иванов", "")
        checkout.click_continue()
        assert checkout.check_error(E_MSG_CHECKOUT_ZIPCODE), "Должна быть ошибка: Postal Code is required"

    def test_check_005(self, logged_in_page):
        # SauceDemo принимает любой формат postal code — документируем поведение
        checkout = self._go_to_step1(logged_in_page)
        checkout.fill_info("Иван", "Иванов", "ABC-XYZ")
        checkout.click_continue()
        checkout.expect_to_have_url(URL_CHECKOUT_STEP2)

    def test_check_006(self, logged_in_page):
        checkout = self._go_to_step1(logged_in_page)
        checkout.click_cancel()
        checkout.expect_to_have_url(URL_CART_HTML)

    def test_check_008(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_btn_add_to_cart()
        logged_in_page.goto(URL_BASE + URL_CART_HTML)
        CartPage(logged_in_page).click_checkout()
        checkout = CheckoutPage(logged_in_page)
        checkout.fill_info("Иван", "Иванов", "12345")
        checkout.click_continue()
        item_total = checkout.get_item_total()
        tax = checkout.get_tax()
        total = checkout.get_total()
        assert abs(total - (item_total + tax)) < 0.01, "Итог должен равняться сумме товаров + налог"

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
        item_total = checkout.get_item_total()
        tax = checkout.get_tax()
        total = checkout.get_total()
        assert abs(total - (item_total + tax)) < 0.01, "Итог должен равняться сумме товаров + налог"
        checkout.click_finish()
        assert checkout.check_order_complete(), "Заказ с несколькими товарами не был оформлен"

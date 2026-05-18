from playwright.sync_api import expect

from config.base import URL_BASE_ROOT, URL_BASE, URL_CART_HTML, URL_CHECKOUT_STEP1, URL_CHECKOUT_STEP2, URL_CHECKOUT_COMPLETE
from config.products import BACKPACK
from config.users import USER1_NAME, USERS_PASSWORD
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestCheckout:

    def test_check_001(self, page):
        page.goto(URL_BASE_ROOT)
        expect(page).to_have_url(URL_BASE_ROOT)
        login_page = LoginPage(page)
        login_page.fill_username(USER1_NAME)
        login_page.check_field_username(USER1_NAME)
        login_page.fill_password(USERS_PASSWORD)
        login_page.check_field_password(USERS_PASSWORD)
        login_page.click_btn_login()
        login_page.expect_to_have_url("/inventory.html")
        inventory_page = InventoryPage(page)
        inventory_page.check_backpack1_visible()
        price1 = inventory_page.get_backpack1_price()
        inventory_page.check_is_price()
        print(f"'{price1}'")
        inventory_page.click_btn_add_to_cart()

    def test_check_002(self, page):
        login_page = LoginPage(page)
        login_page.open()
        login_page.fill_username(USER1_NAME)
        login_page.fill_password(USERS_PASSWORD)
        login_page.click_btn_login()
        login_page.expect_to_have_url("/inventory.html")
        inventory_page = InventoryPage(page)
        inventory_page.click_btn_add_to_cart()
        inventory_page.check_cart_badge("1")

    def test_check_003(self, page):
        login_page = LoginPage(page)
        login_page.open()
        login_page.fill_username(USER1_NAME)
        login_page.fill_password(USERS_PASSWORD)
        login_page.click_btn_login()
        login_page.expect_to_have_url("/inventory.html")
        inventory_page = InventoryPage(page)
        price = inventory_page.get_backpack1_price()
        inventory_page.click_btn_add_to_cart()
        page.goto(URL_BASE + URL_CART_HTML)
        cart_page = CartPage(page)
        cart_page.check_item_visible()
        cart_page.check_item_name(BACKPACK)
        cart_page.check_item_price(price)

    def test_check_004(self, page):
        login_page = LoginPage(page)
        login_page.open()
        login_page.fill_username(USER1_NAME)
        login_page.fill_password(USERS_PASSWORD)
        login_page.click_btn_login()
        login_page.expect_to_have_url("/inventory.html")
        inventory_page = InventoryPage(page)
        inventory_page.click_btn_add_to_cart()
        page.goto(URL_BASE + URL_CART_HTML)
        cart_page = CartPage(page)
        cart_page.check_item_visible()
        cart_page.click_checkout()
        checkout_page = CheckoutPage(page)
        checkout_page.expect_to_have_url(URL_CHECKOUT_STEP1)
        checkout_page.fill_info("Иван", "Иванов", "12345")
        checkout_page.click_continue()
        checkout_page.expect_to_have_url(URL_CHECKOUT_STEP2)
        checkout_page.click_finish()
        checkout_page.expect_to_have_url(URL_CHECKOUT_COMPLETE)
        assert checkout_page.check_order_complete(), "Заказ не был оформлен"

    def test_check_005(self, page):
        login_page = LoginPage(page)
        login_page.open()
        login_page.fill_username(USER1_NAME)
        login_page.fill_password(USERS_PASSWORD)
        login_page.click_btn_login()
        login_page.expect_to_have_url("/inventory.html")
        inventory_page = InventoryPage(page)
        inventory_page.click_btn_add_to_cart()
        inventory_page.check_cart_badge("1")
        page.goto(URL_BASE + URL_CART_HTML)
        cart_page = CartPage(page)
        cart_page.click_remove()
        cart_page.check_cart_is_empty()
        cart_page.check_cart_badge_not_visible()

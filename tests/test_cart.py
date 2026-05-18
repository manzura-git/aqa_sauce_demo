from playwright.sync_api import expect

from config.base import URL_BASE, URL_CART_HTML, URL_INVENTORY
from config.products import BACKPACK, BIKE_LIGHT, BOLT_TSHIRT
from config.users import USER1_NAME, USERS_PASSWORD, USER_PROBLEM_NAME
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestCart:

    def test_cart_001(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_btn_add_to_cart()
        inventory.check_cart_badge("1")

    def test_cart_002(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_add_to_cart_by_name(BACKPACK)
        inventory.click_add_to_cart_by_name(BIKE_LIGHT)
        inventory.click_add_to_cart_by_name(BOLT_TSHIRT)
        inventory.check_cart_badge("3")

    def test_cart_003(self, logged_in_page):
        # Один и тот же товар нельзя добавить дважды — кнопка меняется на Remove
        inventory = InventoryPage(logged_in_page)
        inventory.click_btn_add_to_cart()
        inventory.check_cart_badge("1")
        inventory.check_remove_btn_visible()

    def test_cart_004(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_btn_add_to_cart()
        inventory.check_cart_badge("1")
        inventory.click_remove_backpack()
        inventory.check_cart_badge_not_visible()

    def test_cart_006(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_cart_icon()
        expect(logged_in_page).to_have_url(URL_BASE + URL_CART_HTML)

    def test_cart_007(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_cart_icon()
        cart = CartPage(logged_in_page)
        cart.click_continue_shopping()
        expect(logged_in_page).to_have_url(URL_BASE + URL_INVENTORY)

    def test_cart_008(self, logged_in_page):
        logged_in_page.goto(URL_BASE + URL_CART_HTML)
        cart = CartPage(logged_in_page)
        cart.check_cart_is_empty()

    def test_cart_009(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_btn_add_to_cart()
        inventory.check_cart_badge("1")
        logged_in_page.reload()
        inventory.check_cart_badge("1")

    def test_cart_010(self, page):
        # SauceDemo не изолирует корзину между пользователями — сброс через Reset App State
        login = LoginPage(page)
        login.open()
        login.fill_username(USER1_NAME)
        login.fill_password(USERS_PASSWORD)
        login.click_btn_login()
        login.expect_to_have_url("/inventory.html")
        inventory = InventoryPage(page)
        inventory.click_btn_add_to_cart()
        inventory.check_cart_badge("1")
        inventory.logout()
        login.fill_username(USER_PROBLEM_NAME)
        login.fill_password(USERS_PASSWORD)
        login.click_btn_login()
        login.expect_to_have_url("/inventory.html")
        inventory2 = InventoryPage(page)
        inventory2.open_hamburger_menu()
        page.locator("#reset_sidebar_link").click()
        inventory2.close_hamburger_menu()
        inventory2.check_cart_badge_not_visible()

import allure
import pytest
from playwright.sync_api import expect

from config.base import URL_BASE, URL_CART_HTML, URL_INVENTORY
from config.products import BACKPACK, BIKE_LIGHT, BOLT_TSHIRT
from config.users import USER1_NAME, USERS_PASSWORD, USER_PROBLEM_NAME
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.epic("SauceDemo")
@allure.feature("Корзина")
@pytest.mark.cart
class TestCart:

    @allure.story("TC_CART_001")
    @allure.title("Добавление товара обновляет счётчик корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.high
    def test_cart_001(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_btn_add_to_cart()
        inventory.check_cart_badge("1")

    @allure.story("TC_CART_002")
    @allure.title("Добавление трёх товаров — счётчик показывает 3")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_cart_002(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_add_to_cart_by_name(BACKPACK)
        inventory.click_add_to_cart_by_name(BIKE_LIGHT)
        inventory.click_add_to_cart_by_name(BOLT_TSHIRT)
        inventory.check_cart_badge("3")

    @allure.story("TC_CART_003")
    @allure.title("Один товар нельзя добавить дважды — кнопка меняется")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_cart_003(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_btn_add_to_cart()
        inventory.check_cart_badge("1")
        inventory.check_remove_btn_visible()

    @allure.story("TC_CART_004")
    @allure.title("Удаление товара убирает счётчик")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_cart_004(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_btn_add_to_cart()
        inventory.check_cart_badge("1")
        inventory.click_remove_backpack()
        inventory.check_cart_badge_not_visible()

    @allure.story("TC_CART_006")
    @allure.title("Клик по иконке корзины открывает страницу корзины")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_cart_006(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_cart_icon()
        expect(logged_in_page).to_have_url(URL_BASE + URL_CART_HTML)

    @allure.story("TC_CART_007")
    @allure.title("Continue Shopping возвращает на страницу каталога")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_cart_007(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_cart_icon()
        cart = CartPage(logged_in_page)
        cart.click_continue_shopping()
        expect(logged_in_page).to_have_url(URL_BASE + URL_INVENTORY)

    @allure.story("TC_CART_008")
    @allure.title("Корзина пуста при первом посещении")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_cart_008(self, logged_in_page):
        logged_in_page.goto(URL_BASE + URL_CART_HTML)
        cart = CartPage(logged_in_page)
        cart.check_cart_is_empty()

    @allure.story("TC_CART_009")
    @allure.title("Товар в корзине сохраняется после перезагрузки")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_cart_009(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_btn_add_to_cart()
        inventory.check_cart_badge("1")
        logged_in_page.reload()
        inventory.check_cart_badge("1")

    @allure.story("TC_CART_010")
    @allure.title("Reset App State сбрасывает корзину между пользователями")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_cart_010(self, page):
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
        inventory2.click_reset_app_state()
        inventory2.close_hamburger_menu()
        inventory2.check_cart_badge_not_visible()

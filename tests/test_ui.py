import allure
import pytest
from playwright.sync_api import expect

from config.base import URL_BASE, URL_INVENTORY
from config.users import USER1_NAME, USERS_PASSWORD
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.epic("SauceDemo")
@allure.feature("Интерфейс")
@pytest.mark.ui
class TestUI:

    @allure.story("TC_UI_001")
    @allure.title("Логотип кликабелен — возврат на /inventory.html")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_ui_001(self, logged_in_page):
        """TC_UI_001: логотип кликабелен, возврат на /inventory.html."""
        inventory = InventoryPage(logged_in_page)
        inventory.click_logo()
        expect(logged_in_page).to_have_url(URL_BASE + URL_INVENTORY)

    @allure.story("TC_UI_002")
    @allure.title("Гамбургер-меню открывается и закрывается")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_ui_002(self, logged_in_page):
        """TC_UI_002: гамбургер-меню открывается и закрывается."""
        inventory = InventoryPage(logged_in_page)
        inventory.open_hamburger_menu()
        inventory.check_sidebar_links_visible()
        inventory.close_hamburger_menu()
        inventory.check_sidebar_links_hidden()

    @allure.story("TC_UI_003")
    @allure.title("Мобильная вёрстка 375×667 — элементы доступны")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_ui_003(self, page):
        """TC_UI_003: мобильная вёрстка (375×667) — элементы доступны."""
        page.set_viewport_size({"width": 375, "height": 667})
        login = LoginPage(page)
        login.open()
        login.check_username_field_visible()
        login.check_password_field_visible()
        login.check_login_btn_visible()
        login.fill_username(USER1_NAME)
        login.fill_password(USERS_PASSWORD)
        login.click_btn_login()
        inventory = InventoryPage(page)
        assert inventory.have_title("Products"), (
            "Мобильный вид: заголовок не найден"
        )
        assert inventory.get_item_count() == 6, (
            "Мобильный вид: должно быть 6 товаров"
        )

    @allure.story("TC_UI_006")
    @allure.title("Кнопка Login активна на пустой форме")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_ui_006(self, page):
        """TC_UI_006: кнопка Login активна на пустой форме."""
        login = LoginPage(page)
        login.open()
        login.check_login_btn_enabled()

    @allure.story("TC_UI_007")
    @allure.title("Tab-навигация по полям логина в правильном порядке")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_ui_007(self, page):
        """TC_UI_007: Tab-навигация по полям логина."""
        login = LoginPage(page)
        login.open()
        order = login.get_tab_focus_order()
        assert order == ["user-name", "password", "login-button"]

    @allure.story("TC_UI_008")
    @allure.title("Типы полей, placeholder и alt у изображений корректны")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_ui_008(self, page):
        """TC_UI_008: типы полей, placeholder, alt у изображений."""
        login = LoginPage(page)
        login.open()
        login.check_username_type()
        login.check_password_type()
        login.check_username_placeholder_exists()
        login.check_password_placeholder_exists()
        login.fill_username(USER1_NAME)
        login.fill_password(USERS_PASSWORD)
        login.click_btn_login()
        InventoryPage(page).check_all_images_have_alt()

    @allure.story("TC_UI_009")
    @allure.title("Нет сломанных изображений на странице товаров")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_ui_009(self, logged_in_page):
        """TC_UI_009: нет сломанных изображений на странице товаров."""
        inventory = InventoryPage(logged_in_page)
        inventory.check_images_loaded()
        broken = inventory.get_broken_images_count()
        assert broken == 0, f"Найдено {broken} сломанных изображений"

    @allure.story("TC_UI_010")
    @allure.title("Несуществующий URL возвращает статус 404")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_ui_010(self, logged_in_page):
        """TC_UI_010: несуществующий URL возвращает 404."""
        response = logged_in_page.goto(
            URL_BASE + "/nonexistent-page.html"
        )
        assert response is not None
        assert response.status == 404

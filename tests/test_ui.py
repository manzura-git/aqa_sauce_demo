from playwright.sync_api import expect

from config.base import URL_BASE, URL_INVENTORY
from config.users import USER1_NAME, USERS_PASSWORD
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestUI:

    def test_ui_001(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_logo()
        expect(logged_in_page).to_have_url(URL_BASE + URL_INVENTORY)

    def test_ui_002(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.open_hamburger_menu()
        expect(logged_in_page.locator("#inventory_sidebar_link")).to_be_visible()
        expect(logged_in_page.locator("#about_sidebar_link")).to_be_visible()
        expect(logged_in_page.locator("#logout_sidebar_link")).to_be_visible()
        expect(logged_in_page.locator("#reset_sidebar_link")).to_be_visible()
        inventory.close_hamburger_menu()
        expect(logged_in_page.locator("#inventory_sidebar_link")).not_to_be_visible()

    def test_ui_003(self, page):
        page.set_viewport_size({"width": 375, "height": 667})
        login = LoginPage(page)
        login.open()
        expect(page.locator("#user-name")).to_be_visible()
        expect(page.locator("#password")).to_be_visible()
        expect(page.get_by_role("button", name="Login")).to_be_visible()
        login.fill_username(USER1_NAME)
        login.fill_password(USERS_PASSWORD)
        login.click_btn_login()
        inventory = InventoryPage(page)
        assert inventory.have_title("Products"), "Мобильный вид: заголовок не найден"
        assert page.locator(".inventory_item").count() == 6, "Мобильный вид: должно быть 6 товаров"

    def test_ui_006(self, page):
        login = LoginPage(page)
        login.open()
        expect(page.get_by_role("button", name="Login")).to_be_enabled()

    def test_ui_010(self, logged_in_page):
        response = logged_in_page.goto(URL_BASE + "/nonexistent-page.html")
        assert response is not None
        assert response.status == 404

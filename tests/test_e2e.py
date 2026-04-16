from playwright.sync_api import expect

from config.base import URL_BASE_ROOT
from config.users import USER1_NAME, USERS_PASSWORD
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestCheckout:

    def test_check_001(self, page):
        # Шаг 1 Открыть сайт
        expect(page).to_have_url(URL_BASE_ROOT)
        login_page = LoginPage(page)
        # Шаг 2	Ввести логин
        login_page.fill_username(USER1_NAME)
        login_page.check_field_username(USER1_NAME)
        # Шаг 3	Ввести пароль
        login_page.fill_password(USERS_PASSWORD)
        login_page.check_field_password(USERS_PASSWORD)
        # Шаг 4	Нажать Login
        login_page.click_btn_login()
        login_page.expect_to_have_url("/inventory.html")
        # Шаг 5	Найти товар "Sauce Labs Backpack"
        inventory_page = InventoryPage(page)
        inventory_page.check_backpack1_visible()
        # Шаг 6	Сохранить цену товара
        price1 = inventory_page.get_backpack1_price()
        inventory_page.check_is_price()
        print(f"'{price1}'")
        # Шаг 7	Нажать "Add to cart" для товара
        inventory_page.click_btn_add_to_cart()

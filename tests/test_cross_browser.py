"""TC_XB_*: кросс-браузерные тесты."""
import allure
import pytest
from playwright.sync_api import expect

from config.users import USER1_NAME, USERS_PASSWORD
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

BROWSERS = ["chromium", "firefox", "webkit"]

RESOLUTIONS = [
    (1920, 1080),
    (1366, 768),
    (375, 667),
]


@pytest.fixture(params=BROWSERS, ids=BROWSERS)
def cross_page(request, _playwright):
    """Фикстура: страница в нужном браузере (без asyncio-конфликта)."""
    browser_name = request.param
    browser = getattr(_playwright, browser_name).launch(headless=True)
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 720}
    )
    page = ctx.new_page()
    page.set_default_timeout(10_000)
    yield page, browser_name
    ctx.close()
    browser.close()


def _do_login(page):
    login = LoginPage(page)
    login.open()
    login.fill_username(USER1_NAME)
    login.fill_password(USERS_PASSWORD)
    login.click_btn_login()
    login.expect_to_have_url("/inventory.html")
    return page


@allure.epic("SauceDemo")
@allure.feature("Кросс-браузерность")
@pytest.mark.cross_browser
class TestCrossBrowser:

    @allure.story("TC_XB_001/002/003")
    @allure.title("Базовый сценарий: логин и каталог в каждом браузере")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.high
    def test_xb_001_003_login_and_inventory(self, cross_page):
        """TC_XB_001/002/003: базовый сценарий в каждом браузере."""
        page, browser_name = cross_page
        _do_login(page)
        inventory = InventoryPage(page)
        assert inventory.have_title("Products"), (
            f"{browser_name}: заголовок 'Products' не найден"
        )
        assert inventory.get_item_count() == 6, (
            f"{browser_name}: должно быть 6 товаров"
        )

    @allure.story("TC_XB_001/002/003")
    @allure.title("Добавление в корзину в каждом браузере")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_xb_001_003_add_to_cart(self, cross_page):
        """TC_XB_001/002/003: добавление в корзину в каждом браузере."""
        page, browser_name = cross_page
        _do_login(page)
        inventory = InventoryPage(page)
        inventory.click_btn_add_to_cart()
        inventory.check_cart_badge("1")
        inventory.click_remove_backpack()
        inventory.check_cart_badge_not_visible()


    @allure.story("TC_XB_005")
    @allure.title("UI корректен при разных разрешениях экрана")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    @pytest.mark.parametrize("width,height", RESOLUTIONS, ids=[
        "1920x1080", "1366x768", "375x667_mobile"
    ])
    def test_xb_005_resolutions(self, _playwright, width, height):
        """TC_XB_005: проверка UI при разных разрешениях экрана."""
        browser = _playwright.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": width, "height": height}
        )
        page = ctx.new_page()
        page.set_default_timeout(8_000)
        try:
            _do_login(page)
            inventory = InventoryPage(page)
            assert inventory.have_title("Products"), (
                f"{width}x{height}: заголовок не найден"
            )
            assert inventory.get_item_count() == 6, (
                f"{width}x{height}: должно быть 6 товаров"
            )
            inventory.check_hamburger_btn_visible()
        finally:
            ctx.close()
            browser.close()

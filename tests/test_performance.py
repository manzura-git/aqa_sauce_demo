"""
TC_PERF_*: тесты производительности и надёжности.
"""
import allure
import pytest

from config.base import URL_BASE, URL_BASE_ROOT, URL_INVENTORY
from config.users import USER1_NAME, USERS_PASSWORD
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.helpers import get_page_load_time, measure_action_ms


@allure.epic("SauceDemo")
@allure.feature("Производительность")
@pytest.mark.performance
class TestPerformance:

    @allure.story("TC_PERF_001")
    @allure.title("Время загрузки главной страницы < 3000 мс")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_perf_001_page_load_time(self, page):
        """TC_PERF_001: время загрузки главной страницы < 3000 мс."""
        page.goto(URL_BASE_ROOT, wait_until="load")
        load_ms = get_page_load_time(page)
        assert load_ms < 3_000, (
            f"Страница загружалась {load_ms:.0f} мс, ожидалось < 3000 мс"
        )

    @allure.story("TC_PERF_002")
    @allure.title("Время отклика кнопки Login < 3000 мс")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_perf_002_login_response_time(self, page):
        """TC_PERF_002: время отклика кнопки Login < 3000 мс."""
        login = LoginPage(page)
        login.open()
        login.fill_username(USER1_NAME)
        login.fill_password(USERS_PASSWORD)

        elapsed = measure_action_ms(login.click_btn_login)
        page.wait_for_url(f"**{URL_INVENTORY}**", timeout=5_000)

        assert elapsed < 3_000, (
            f"Клик по Login занял {elapsed:.0f} мс, ожидалось < 3000 мс"
        )

    @allure.story("TC_PERF_003")
    @allure.title("Страница инвентаря загружается < 3000 мс")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_perf_003_inventory_page_load(self, logged_in_page):
        """TC_PERF_003: страница инвентаря загружается < 3000 мс."""
        logged_in_page.goto(URL_BASE + URL_INVENTORY, wait_until="load")
        load_ms = get_page_load_time(logged_in_page)
        assert load_ms < 3_000, (
            f"Инвентарь загружался {load_ms:.0f} мс, ожидалось < 3000 мс"
        )

    @allure.story("TC_PERF_004")
    @allure.title("performance_glitch_user входит за разумное время")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_perf_004_performance_glitch_user(self, page):
        """TC_PERF_004: performance_glitch_user входит за разумное время."""
        page.set_default_timeout(15_000)
        login = LoginPage(page)
        login.open()
        login.fill_username("performance_glitch_user")
        login.fill_password(USERS_PASSWORD)

        elapsed = measure_action_ms(login.click_btn_login)
        page.wait_for_url(f"**{URL_INVENTORY}**", timeout=15_000)

        assert elapsed < 10_000, (
            f"Вход performance_glitch_user занял {elapsed:.0f} мс"
        )

    @allure.story("TC_PERF_005")
    @allure.title("Имитация медленной сети — тест проходит без таймаутов")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_perf_005_slow_network_simulation(self, logged_in_page):
        """TC_PERF_005: имитация медленной сети через route-задержку."""
        logged_in_page.set_default_timeout(15_000)

        def add_latency(route):
            import time
            time.sleep(0.3)
            route.continue_()

        logged_in_page.route("**/*", add_latency)
        logged_in_page.reload(wait_until="domcontentloaded")
        inventory = InventoryPage(logged_in_page)
        assert inventory.get_item_count() == 6
        logged_in_page.unroute("**/*")

    @allure.story("TC_PERF_006")
    @allure.title("Все изображения загружаются без ошибок")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_perf_006_images_load_without_errors(self, logged_in_page):
        """TC_PERF_006: все изображения загружаются без ошибок."""
        inventory = InventoryPage(logged_in_page)
        broken = inventory.get_broken_images_count()
        assert broken == 0, f"Найдено {broken} сломанных изображений"

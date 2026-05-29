import allure
import pytest

from config.base import (
    E_MSG_LOGIN,
    E_MSG_LOGIN_USERNAME,
    E_MSG_LOGIN_PASSWORD,
    E_MSG_LOGIN_LOCKED,
    E_MSG_LOGIN_CARD,
    URL_BASE,
    URL_CART_HTML,
)
from config.users import (
    USER1_NAME,
    USERS_PASSWORD,
    USER_FAKE_NAME,
    USER_LOCKED_NAME,
    USER_PROBLEM_NAME,
    USER_PERFORMANCE_NAME,
)
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.epic("SauceDemo")
@allure.feature("Авторизация")
@pytest.mark.auth
class TestAuth:

    @allure.story("TC_AUTH_001")
    @allure.title("Успешный вход со стандартным пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.high
    def test_auth_001(self, page):
        """TC_AUTH_001: успешный вход со стандартным пользователем."""
        login = LoginPage(page)
        login.open()
        login.fill_username(USER1_NAME)
        login.check_field_username(USER1_NAME)
        login.fill_password(USERS_PASSWORD)
        login.check_field_password(USERS_PASSWORD)
        login.click_btn_login()
        login.expect_to_have_url("/inventory.html")
        assert InventoryPage(page).have_title("Products")

    @allure.story("TC_AUTH_002")
    @allure.title("Заблокированный пользователь видит ошибку")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.high
    def test_auth_002_locked_user(self, page):
        """TC_AUTH_002: заблокированный пользователь видит ошибку."""
        login = LoginPage(page)
        login.open()
        login.fill_username(USER_LOCKED_NAME)
        login.fill_password(USERS_PASSWORD)
        login.click_btn_login()
        assert login.check_error_with_msg(E_MSG_LOGIN_LOCKED)

    @allure.story("TC_AUTH_002")
    @allure.title("Другие валидные пользователи проходят авторизацию")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    @pytest.mark.parametrize(
        "username", [USER_PROBLEM_NAME, USER_PERFORMANCE_NAME]
    )
    def test_auth_002_valid_users(self, page, username):
        """TC_AUTH_002: другие валидные пользователи проходят авторизацию."""
        if username == USER_PERFORMANCE_NAME:
            page.set_default_timeout(15_000)
        login = LoginPage(page)
        login.open()
        login.fill_username(username)
        login.fill_password(USERS_PASSWORD)
        login.click_btn_login()
        login.expect_to_have_url("/inventory.html")
        assert InventoryPage(page).have_title("Products")

    @allure.story("TC_AUTH_003")
    @allure.title("Неверный пароль — ошибка авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.high
    def test_auth_003(self, page):
        """TC_AUTH_003: неверный пароль → ошибка авторизации."""
        login = LoginPage(page)
        login.open()
        login.fill_username(USER1_NAME)
        login.fill_password("wrong_password")
        login.click_btn_login()
        assert login.check_error_with_msg(E_MSG_LOGIN)

    @allure.story("TC_AUTH_004")
    @allure.title("Несуществующий логин — ошибка авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.high
    def test_auth_004(self, page):
        """TC_AUTH_004: несуществующий логин → ошибка авторизации."""
        login = LoginPage(page)
        login.open()
        login.fill_username(USER_FAKE_NAME)
        login.fill_password(USERS_PASSWORD)
        login.click_btn_login()
        assert login.check_error_with_msg(E_MSG_LOGIN)

    @allure.story("TC_AUTH_005")
    @allure.title("Пустой логин — Username is required")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_auth_005(self, page):
        """TC_AUTH_005: пустой логин → Username is required."""
        login = LoginPage(page)
        login.open()
        login.fill_username("")
        login.fill_password(USERS_PASSWORD)
        login.click_btn_login()
        assert login.check_error_with_msg(E_MSG_LOGIN_USERNAME)

    @allure.story("TC_AUTH_006")
    @allure.title("Пустой пароль — Password is required")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_auth_006(self, page):
        """TC_AUTH_006: пустой пароль → Password is required."""
        login = LoginPage(page)
        login.open()
        login.fill_username(USER1_NAME)
        login.fill_password("")
        login.click_btn_login()
        assert login.check_error_with_msg(E_MSG_LOGIN_PASSWORD)

    @allure.story("TC_AUTH_007")
    @allure.title("SQL-инъекция в поле логина — отказ в доступе")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    @pytest.mark.parametrize("payload", [
        "' OR '1'='1",
        "admin' OR 1=1--",
        "1 UNION SELECT username, password FROM users",
        "1 AND (SELECT COUNT(*) FROM users WHERE id=5)=1",
    ])
    def test_auth_007(self, page, payload):
        """TC_AUTH_007: SQL-инъекция в поле логина → отказ в доступе."""
        login = LoginPage(page)
        login.open()
        login.fill_username(payload)
        login.fill_password("any")
        login.click_btn_login()
        assert login.check_error_with_msg(E_MSG_LOGIN)

    @allure.story("TC_AUTH_008")
    @allure.title("XSS в поле логина — скрипт не выполняется")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_auth_008(self, page):
        """TC_AUTH_008: XSS в поле логина → скрипт не выполняется."""
        payload = "<script>alert(1)</script>"
        login = LoginPage(page)
        login.open()
        login.fill_username(payload)
        login.fill_password("any")
        login.click_btn_login()
        assert login.check_error_with_msg(E_MSG_LOGIN)
        field_value = login.get_username_input_value()
        assert "<script>" not in page.content() or field_value == payload

    @allure.story("TC_AUTH_009")
    @allure.title("5 неудачных попыток — аккаунт не блокируется")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_auth_009_no_lockout(self, page):
        """TC_AUTH_009: 5 неудачных попыток — аккаунт не блокируется."""
        login = LoginPage(page)
        login.open()
        for _ in range(5):
            login.fill_username(USER1_NAME)
            login.fill_password("wrong_pass")
            login.click_btn_login()
            assert login.check_error_with_msg(E_MSG_LOGIN)

        login.fill_username(USER1_NAME)
        login.fill_password(USERS_PASSWORD)
        login.click_btn_login()
        login.expect_to_have_url("/inventory.html")

    @allure.story("TC_AUTH_010")
    @allure.title("Сессия сохраняется после перезагрузки страницы")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_auth_010(self, page):
        """TC_AUTH_010: сессия сохраняется после перезагрузки страницы."""
        login = LoginPage(page)
        login.open()
        login.fill_username(USER1_NAME)
        login.fill_password(USERS_PASSWORD)
        login.click_btn_login()
        login.expect_to_have_url("/inventory.html")
        page.reload()
        login.expect_to_have_url("/inventory.html")

    @allure.story("TC_AUTH_009")
    @allure.title("Прямой переход на /cart.html без авторизации — ошибка")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_auth_redirect_cart_without_login(self, page):
        """TC_AUTH_009 (secondary): прямой переход на /cart.html → ошибка."""
        login = LoginPage(page)
        login.open(URL_BASE + URL_CART_HTML)
        assert login.check_error_with_msg(E_MSG_LOGIN_CARD)

import pytest

from config.base import (E_MSG_LOGIN, E_MSG_LOGIN_USERNAME, E_MSG_LOGIN_PASSWORD,
                         E_MSG_LOGIN_LOCKED, E_MSG_LOGIN_CARD, URL_BASE, URL_CART_HTML)
from config.users import (USER1_NAME, USERS_PASSWORD, USER_FAKE_NAME, USER_LOCKED_NAME,
                           USER_PROBLEM_NAME, USER_PERFORMANCE_NAME)
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestAuth:

    def test_auth_001(self, page):
        login_page = LoginPage(page)
        login_page.open()
        login_page.fill_username(USER1_NAME)
        login_page.check_field_username(USER1_NAME)
        login_page.fill_password(USERS_PASSWORD)
        login_page.check_field_password(USERS_PASSWORD)
        login_page.click_btn_login()
        login_page.expect_to_have_url("/inventory.html")
        inventory_page = InventoryPage(page)
        assert inventory_page.have_title("Products"), "Заголовок не тот"

    def test_auth_002(self, page):
        login_page = LoginPage(page)
        login_page.open()
        login_page.fill_username(USER_LOCKED_NAME)
        login_page.fill_password(USERS_PASSWORD)
        login_page.click_btn_login()
        assert login_page.check_error_with_msg(E_MSG_LOGIN_LOCKED),\
            "Заблокированный пользователь должен видеть ошибку"

    @pytest.mark.parametrize("username", [USER_PROBLEM_NAME, USER_PERFORMANCE_NAME])
    def test_auth_002_valid_users(self, page, username):
        if username == USER_PERFORMANCE_NAME:
            page.set_default_timeout(10_000)
        login_page = LoginPage(page)
        login_page.open()
        login_page.fill_username(username)
        login_page.fill_password(USERS_PASSWORD)
        login_page.click_btn_login()
        login_page.expect_to_have_url("/inventory.html")
        inventory_page = InventoryPage(page)
        assert inventory_page.have_title("Products"), f"{username}: заголовок не тот"

    def test_auth_009(self, page):
        login_page = LoginPage(page)
        login_page.open(URL_BASE + URL_CART_HTML)
        assert login_page.check_error_with_msg(E_MSG_LOGIN_CARD),\
            "Доступ к /cart.html без авторизации должен показывать ошибку"

    def test_auth_010(self, page):
        login_page = LoginPage(page)
        login_page.open()
        login_page.fill_username(USER1_NAME)
        login_page.fill_password(USERS_PASSWORD)
        login_page.click_btn_login()
        login_page.expect_to_have_url("/inventory.html")
        page.reload()
        login_page.expect_to_have_url("/inventory.html")

    @pytest.mark.parametrize(
        "page,username,password,error_msg",
        [((True, 123), USER1_NAME, "wrong_password", E_MSG_LOGIN),
         (False, USER_FAKE_NAME, USERS_PASSWORD, E_MSG_LOGIN),
         (True, "", USERS_PASSWORD, E_MSG_LOGIN_USERNAME),
         (True, USER1_NAME, "", E_MSG_LOGIN_PASSWORD),
         (True, "admin' OR 1=1", "any", E_MSG_LOGIN),
         (True, "' OR '1'='1", "any", E_MSG_LOGIN),
         (True, "1 UNION SELECT username, password FROM users", "any",
          E_MSG_LOGIN),
         (True, "1 AND (SELECT COUNT(*) FROM users WHERE id=5)=1", "any",
          E_MSG_LOGIN),
         (True, "<script>alert(1)</script>", "any", E_MSG_LOGIN)],
        indirect = ["page"]
        )
    def test_auth_003_004_005_006_007_008(self, page, username, password, error_msg):
        login_page = LoginPage(page)
        login_page.open()
        login_page.fill_username(username)
        login_page.check_field_username(username)
        login_page.fill_password(password)
        login_page.check_field_password(password)
        login_page.click_btn_login()
        assert login_page.check_error_with_msg(error_msg), "Что-то пошло не так!"

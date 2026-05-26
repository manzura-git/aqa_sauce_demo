import pytest
from playwright.sync_api import sync_playwright

from config.base import URL_BASE
from config.users import USER1_NAME, USERS_PASSWORD


@pytest.fixture
def page(request):
    if hasattr(request, "param"):
        if isinstance(request.param, tuple):
            headless_ = request.param[0]
        else:
            headless_ = request.param
    with sync_playwright() as drv:
        browser = drv.chromium.launch(headless=True, slow_mo=500)
        page = browser.new_page()
        page.set_default_timeout(8_000)
        yield page
        browser.close()

@pytest.fixture
def logged_in_page(page):
    from pages.login_page import LoginPage
    login = LoginPage(page)
    login.open()
    login.fill_username(USER1_NAME)
    login.fill_password(USERS_PASSWORD)
    login.click_btn_login()
    login.expect_to_have_url("/inventory.html")
    return page

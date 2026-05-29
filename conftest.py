import os

import allure
import pytest
from playwright.sync_api import sync_playwright

from config.base import URL_BASE
from config.users import USER1_NAME, USERS_PASSWORD

for _d in (
    "output/screenshots",
    "output/videos",
    "output/logs",
    "output/reports/allure-results",
):
    os.makedirs(_d, exist_ok=True)


def pytest_addoption(parser):
    parser.addoption(
        "--browser-name",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Браузер для запуска тестов",
    )
    parser.addoption(
        "--slow-mo",
        type=int,
        default=0,
        help="Задержка между действиями (мс)",
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session")
def _playwright():
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(_playwright, request):
    name = request.config.getoption("--browser-name")
    headed = request.config.getoption("--headed", default=False)
    slow_mo = request.config.getoption("--slow-mo")
    br = getattr(_playwright, name).launch(
        headless=not headed,
        slow_mo=slow_mo,
    )
    yield br
    br.close()


@pytest.fixture
def context(browser):
    ctx = browser.new_context(viewport={"width": 1280, "height": 720})
    yield ctx
    ctx.close()


@pytest.fixture
def page(context, request):
    p = context.new_page()
    p.set_default_timeout(8_000)
    yield p
    failed = (
        hasattr(request.node, "rep_call")
        and request.node.rep_call.failed
    )
    if failed:
        safe_name = request.node.name.replace("/", "_").replace(":", "_")
        screenshot_path = f"output/screenshots/{safe_name}.png"
        p.screenshot(path=screenshot_path)
        allure.attach(
            p.screenshot(),
            name=safe_name,
            attachment_type=allure.attachment_type.PNG,
        )


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

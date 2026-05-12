import pytest
from playwright.sync_api import sync_playwright

from config.base import URL_BASE


@pytest.fixture
def page(request):
    if hasattr(request, "param"):
        if isinstance(request.param, tuple):
            headless_ = request.param[0]
        else:
            headless_ = request.param
    else:
        headless_ = False
    with sync_playwright() as drv:
        browser = drv.chromium.launch(headless=headless_, slow_mo=500)
        page = browser.new_page()
        page.set_default_timeout(4_000)
        yield page
        browser.close()

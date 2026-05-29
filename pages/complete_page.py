import allure
from playwright.sync_api import expect

from config.base import MSG_ORDER_COMPLETE, MSG_ORDER_DISPATCHED
from pages.base_page import BasePage


class CompletePage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.header = self.page.locator(".complete-header")
        self.text = self.page.locator(".complete-text")
        self.back_btn = self.page.get_by_role("button", name="Back Home")

    @allure.step("Проверить страницу завершения заказа")
    def check_order_complete(self):
        expect(self.header).to_be_visible()
        expect(self.header).to_have_text(MSG_ORDER_COMPLETE)
        expect(self.text).to_contain_text(MSG_ORDER_DISPATCHED)
        return True

    @allure.step("Нажать Back Home")
    def click_back_home(self):
        self.back_btn.click()

from playwright.sync_api import expect

from config.base import E_MSG_LOGIN
from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.field_username = self.page.locator("#user-name")
        self.field_password = self.page.locator("#password")
        # self.btn_login = self.page.locator("[data-test='login-button']")
        # self.btn_login = self.page.get_by_test_id("login-button")
        self.btn_login = self.page.get_by_role("button", name="Login")
        self.error = self.page.locator(".error-message-container")

    def fill_username(self, username):
        self.field_username.fill(username)

    def fill_password(self, password):
        self.field_password.fill(password)

    def click_btn_login(self):
        self.btn_login.click()

    def check_field_username(self, username):
        expect(self.field_username).to_have_value(username)

    def check_field_password(self, password):
        expect(self.field_password).to_have_value(password)

    def check_error_with_msg(self, error_msg=E_MSG_LOGIN):
        # expect(self.error).to_have_element(".error-message")
        expect(self.error).to_be_visible()
        expect(self.error).to_have_text(error_msg)
        return True

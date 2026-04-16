from playwright.sync_api import expect

from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.field_username = self.page.locator("#user-name")
        self.field_password = self.page.locator("#password")
        # self.btn_login = self.page.locator("[data-test='login-button']")
        # self.btn_login = self.page.get_by_test_id("login-button")
        self.btn_login = self.page.get_by_role("button", name="Login")

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

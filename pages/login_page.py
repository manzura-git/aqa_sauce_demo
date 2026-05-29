import allure
from playwright.sync_api import expect

from config.base import E_MSG_LOGIN
from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.field_username = self.page.locator("#user-name")
        self.field_password = self.page.locator("#password")
        self.btn_login = self.page.get_by_role("button", name="Login")
        self.error = self.page.locator(".error-message-container")

    # --- заполнение ---

    @allure.step("Ввод логина: {username}")
    def fill_username(self, username):
        self.field_username.fill(username)

    @allure.step("Ввод пароля")
    def fill_password(self, password):
        self.field_password.fill(password)

    @allure.step("Нажать кнопку Login")
    def click_btn_login(self):
        self.btn_login.click()

    # --- проверки полей ---

    @allure.step("Проверить значение поля Username: {username}")
    def check_field_username(self, username):
        expect(self.field_username).to_have_value(username)

    @allure.step("Проверить значение поля Password")
    def check_field_password(self, password):
        expect(self.field_password).to_have_value(password)

    @allure.step("Проверить видимость поля Username")
    def check_username_field_visible(self):
        expect(self.field_username).to_be_visible()

    @allure.step("Проверить видимость поля Password")
    def check_password_field_visible(self):
        expect(self.field_password).to_be_visible()

    @allure.step("Проверить видимость кнопки Login")
    def check_login_btn_visible(self):
        expect(self.btn_login).to_be_visible()

    @allure.step("Проверить активность кнопки Login")
    def check_login_btn_enabled(self):
        expect(self.btn_login).to_be_enabled()

    @allure.step("Проверить тип поля Username")
    def check_username_type(self):
        assert self.field_username.get_attribute("type") == "text"

    @allure.step("Проверить тип поля Password")
    def check_password_type(self):
        assert self.field_password.get_attribute("type") == "password"

    @allure.step("Проверить наличие placeholder в поле Username")
    def check_username_placeholder_exists(self):
        assert self.field_username.get_attribute("placeholder") is not None

    @allure.step("Проверить наличие placeholder в поле Password")
    def check_password_placeholder_exists(self):
        assert self.field_password.get_attribute("placeholder") is not None

    def get_username_input_value(self) -> str:
        return self.field_username.input_value()

    # --- Tab-навигация ---

    @allure.step("Получить порядок Tab-фокуса")
    def get_tab_focus_order(self) -> list:
        """Нажимает Tab три раза и возвращает список id сфокусированных элементов."""
        order = []
        for _ in range(3):
            self.page.keyboard.press("Tab")
            order.append(
                self.page.evaluate("document.activeElement.id")
            )
        return order

    # --- ошибки ---

    @allure.step("Проверить сообщение об ошибке")
    def check_error_with_msg(self, error_msg=E_MSG_LOGIN):
        expect(self.error).to_be_visible()
        expect(self.error).to_have_text(error_msg)
        return True

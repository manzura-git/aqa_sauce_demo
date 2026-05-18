from playwright.sync_api import expect

from pages.base_page import BasePage


class CheckoutPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.field_first_name = self.page.locator("#first-name")
        self.field_last_name = self.page.locator("#last-name")
        self.field_zip = self.page.locator("#postal-code")
        self.btn_continue = self.page.get_by_role("button", name="Continue")
        self.btn_finish = self.page.get_by_role("button", name="Finish")
        self.btn_cancel = self.page.get_by_role("button", name="Cancel")
        self.complete_header = self.page.locator(".complete-header")
        self.error_message = self.page.locator("[data-test='error']")

    def fill_info(self, first_name: str, last_name: str, zip_code: str):
        self.field_first_name.fill(first_name)
        self.field_last_name.fill(last_name)
        self.field_zip.fill(zip_code)

    def click_continue(self):
        self.btn_continue.click()

    def click_finish(self):
        self.btn_finish.click()

    def click_cancel(self):
        self.btn_cancel.click()

    def check_order_complete(self):
        expect(self.complete_header).to_be_visible()
        expect(self.complete_header).to_have_text("Thank you for your order!")
        return True

    def check_error(self, msg: str):
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_have_text(msg)
        return True

    def get_item_total(self) -> float:
        text = self.page.locator(".summary_subtotal_label").text_content()
        return float(text.split("$")[1])

    def get_tax(self) -> float:
        text = self.page.locator(".summary_tax_label").text_content()
        return float(text.split("$")[1])

    def get_total(self) -> float:
        text = self.page.locator(".summary_total_label").text_content()
        return float(text.split("$")[1])

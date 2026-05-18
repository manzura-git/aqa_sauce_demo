import re

from playwright.sync_api import expect

from config.base import SORT_AZ, SORT_PRICE_LOW, SORT_PRICE_HIGH
from config.products import BACKPACK, EXPECTED_PRODUCTS, EXPECTED_PRICES
from pages.inventory_page import InventoryPage


class TestInventory:

    def test_inv_001(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        assert inventory.get_item_count() == 6, "На странице должно быть 6 товаров"

    def test_inv_002(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        names = inventory.get_all_names()
        assert sorted(names) == sorted(EXPECTED_PRODUCTS), "Названия товаров не совпадают с ожидаемыми"

    def test_inv_003(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        names = inventory.get_all_names()
        prices = logged_in_page.locator(".inventory_item_price").all_text_contents()
        actual = dict(zip(names, prices))
        for product, expected_price in EXPECTED_PRICES.items():
            assert actual[product] == expected_price, f"Цена {product}: ожидалась {expected_price}, получена {actual[product]}"

    def test_inv_004(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.check_images_loaded()

    def test_inv_005(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.select_sort(SORT_PRICE_LOW)
        prices = inventory.get_all_prices()
        assert prices == sorted(prices), "Цены должны идти по возрастанию"

    def test_inv_006(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.select_sort(SORT_PRICE_HIGH)
        prices = inventory.get_all_prices()
        assert prices == sorted(prices, reverse=True), "Цены должны идти по убыванию"

    def test_inv_007(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.select_sort(SORT_AZ)
        names = inventory.get_all_names()
        assert names == sorted(names), "Названия должны быть отсортированы по алфавиту A→Z"

    def test_inv_008(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_btn_add_to_cart()
        inventory.check_cart_badge("1")
        inventory.select_sort(SORT_PRICE_HIGH)
        inventory.check_remove_btn_visible()

    def test_inv_009(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_backpack_image()
        expect(logged_in_page).to_have_url(re.compile(r"inventory-item\.html"))

    def test_inv_010(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_btn_add_to_cart()
        inventory.check_remove_btn_visible()
        inventory.click_remove_backpack()
        inventory.check_cart_badge_not_visible()

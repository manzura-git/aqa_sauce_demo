import re

import allure
import pytest
from playwright.sync_api import expect

from config.base import SORT_AZ, SORT_PRICE_LOW, SORT_PRICE_HIGH
from config.products import BACKPACK, EXPECTED_PRODUCTS, EXPECTED_PRICES
from pages.inventory_page import InventoryPage
from utils.assertions import (
    assert_prices_sorted_asc,
    assert_prices_sorted_desc,
    assert_names_sorted_asc,
)


@allure.epic("SauceDemo")
@allure.feature("Каталог товаров")
@pytest.mark.inventory
class TestInventory:

    @allure.story("TC_INV_001")
    @allure.title("На странице отображается 6 товаров")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.high
    def test_inv_001(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        assert inventory.get_item_count() == 6, (
            "На странице должно быть 6 товаров"
        )

    @allure.story("TC_INV_002")
    @allure.title("Названия товаров совпадают с ожидаемыми")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_inv_002(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        names = inventory.get_all_names()
        assert sorted(names) == sorted(EXPECTED_PRODUCTS), \
            "Названия товаров не совпадают с ожидаемыми"

    @allure.story("TC_INV_003")
    @allure.title("Цены товаров совпадают с ожидаемыми")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_inv_003(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        names = inventory.get_all_names()
        prices = inventory.get_all_prices_text()
        actual = dict(zip(names, prices))
        for product, expected_price in EXPECTED_PRICES.items():
            assert actual[product] == expected_price, (
                f"Цена {product}: ожидалась {expected_price},"
                f" получена {actual[product]}"
            )

    @allure.story("TC_INV_004")
    @allure.title("Все изображения товаров загружаются")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_inv_004(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.check_images_loaded()

    @allure.story("TC_INV_005")
    @allure.title("Сортировка по цене: от низкой к высокой")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_inv_005(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.select_sort(SORT_PRICE_LOW)
        assert_prices_sorted_asc(inventory.get_all_prices(), "TC_INV_005")

    @allure.story("TC_INV_006")
    @allure.title("Сортировка по цене: от высокой к низкой")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_inv_006(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.select_sort(SORT_PRICE_HIGH)
        assert_prices_sorted_desc(inventory.get_all_prices(), "TC_INV_006")

    @allure.story("TC_INV_007")
    @allure.title("Сортировка по алфавиту: A → Z")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_inv_007(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.select_sort(SORT_AZ)
        assert_names_sorted_asc(inventory.get_all_names(), "TC_INV_007")

    @allure.story("TC_INV_008")
    @allure.title("Кнопка Remove остаётся после смены сортировки")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_inv_008(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_btn_add_to_cart()
        inventory.check_cart_badge("1")
        inventory.select_sort(SORT_PRICE_HIGH)
        inventory.check_remove_btn_visible()

    @allure.story("TC_INV_009")
    @allure.title("Клик по изображению открывает страницу товара")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_inv_009(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_backpack_image()
        expect(logged_in_page).to_have_url(
            re.compile(r"inventory-item\.html")
        )

    @allure.story("TC_INV_010")
    @allure.title("Удаление товара из корзины через кнопку Remove")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_inv_010(self, logged_in_page):
        inventory = InventoryPage(logged_in_page)
        inventory.click_btn_add_to_cart()
        inventory.check_remove_btn_visible()
        inventory.click_remove_backpack()
        inventory.check_cart_badge_not_visible()

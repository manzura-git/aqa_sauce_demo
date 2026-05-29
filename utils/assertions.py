def assert_prices_sorted_asc(prices: list[float], label: str = ""):
    msg = f"{label}: цены должны идти по возрастанию. Получено: {prices}"
    assert prices == sorted(prices), msg


def assert_prices_sorted_desc(prices: list[float], label: str = ""):
    msg = f"{label}: цены должны идти по убыванию. Получено: {prices}"
    assert prices == sorted(prices, reverse=True), msg


def assert_names_sorted_asc(names: list[str], label: str = ""):
    msg = f"{label}: имена должны быть отсортированы A→Z. Получено: {names}"
    assert names == sorted(names), msg


def assert_total_equals_subtotal_plus_tax(
    subtotal: float,
    tax: float,
    total: float,
    tolerance: float = 0.01,
):
    expected = round(subtotal + tax, 2)
    diff = abs(total - expected)
    assert diff < tolerance, (
        f"Итог {total} ≠ subtotal {subtotal} + tax {tax} = {expected}"
    )


def assert_item_count(actual: int, expected: int, label: str = ""):
    msg = f"{label}: ожидалось {expected} товаров, найдено {actual}"
    assert actual == expected, msg


def assert_badge_text(actual: str, expected: str):
    assert actual == expected, (
        f"Бейдж корзины: ожидалось '{expected}', получено '{actual}'"
    )

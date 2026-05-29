import time


def parse_price(text: str) -> float:
    """Преобразует '$29.99' → 29.99."""
    return float(text.strip().replace("$", ""))


def format_price(value: float) -> str:
    """Преобразует 29.99 → '$29.99'."""
    return f"${value:.2f}"


def get_page_load_time(page) -> float:
    """Возвращает время загрузки страницы через Navigation Timing API (мс)."""
    timing = page.evaluate(
        "() => {"
        "  const t = performance.timing;"
        "  return t.loadEventEnd - t.navigationStart;"
        "}"
    )
    return float(timing)


def measure_action_ms(fn) -> float:
    """Выполняет fn() и возвращает время выполнения в мс."""
    start = time.monotonic()
    fn()
    return (time.monotonic() - start) * 1_000


def wait_for_url_contains(page, substring: str, timeout: int = 5_000):
    page.wait_for_url(f"**{substring}**", timeout=timeout)

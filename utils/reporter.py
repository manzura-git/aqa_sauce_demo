import allure


def step(title: str):
    """Декоратор / контекст-менеджер для Allure-шага."""
    return allure.step(title)


def attach_screenshot(page, name: str = "screenshot"):
    allure.attach(
        page.screenshot(),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )


def attach_text(content: str, name: str = "info"):
    allure.attach(
        content,
        name=name,
        attachment_type=allure.attachment_type.TEXT,
    )

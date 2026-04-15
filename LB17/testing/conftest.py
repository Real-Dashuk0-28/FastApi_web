import os


if os.getenv("TESTING") != "1":
    raise RuntimeError(
        "Окружение не готово для тестов. "
        "Установите TESTING=1 перед запуском pytest."
    )

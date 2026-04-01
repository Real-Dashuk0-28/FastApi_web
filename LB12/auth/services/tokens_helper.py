from abc import ABC, abstractmethod


class AbstractTokensHelper(ABC):
    @abstractmethod
    def token_exists(self, token: str) -> bool:
        """Проверка наличия токена"""
        pass

    @abstractmethod
    def add_token(self, token: str) -> None:
        """Добавление токена в хранилище"""
        pass

    @abstractmethod
    def generate_and_save_token(self) -> str:
        """Генерация нового токена"""
        pass

    @abstractmethod
    def get_tokens(self) -> list[str]:  # ← новый абстрактный метод
        """Получение списка всех токенов"""
        pass
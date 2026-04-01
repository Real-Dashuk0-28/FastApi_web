from abc import ABC, abstractmethod
import bcrypt


class AbstractUserHelper(ABC):
    @abstractmethod
    def get_user_password(self, username: str) -> str:
        """Получение пароля по имени пользователя"""
        pass

    def check_passwords_match(self, password: str, hashed_password: str) -> bool:
        """
        Сравнение пароля с хешем
        Возвращает True, если совпадают, иначе False
        """
        if not password or not hashed_password:
            return False
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )

    def validate_user_password(self, username: str, password: str) -> bool:
        """
        Проверка совпадения переданного пароля с тем, что в базе
        """
        stored_password = self.get_user_password(username)
        if not stored_password:
            return False
        return self.check_passwords_match(password, stored_password)
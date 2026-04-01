import redis
import bcrypt
from ....core import config
from .users_helper import AbstractUserHelper


class RedisUserHelper(AbstractUserHelper):
    def __init__(self):
        self.redis = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_USER_DB,
            decode_responses=True
        )

    def get_user_password(self, username: str) -> str | None:  # ✅ Добавляем тип None
        """Получение хеша пароля пользователя"""
        return self.redis.get(f"user:{username}:password")

    def add_user(self, username: str, password: str) -> None:
        """
        Добавление пользователя (пароль хешируется)
        Используйте этот метод для добавления тестовых пользователей
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.redis.set(f"user:{username}:password", hashed.decode('utf-8'))

    def user_exists(self, username: str) -> bool:
        """Проверка существования пользователя"""
        return self.redis.exists(f"user:{username}:password") > 0
import redis
import secrets
from core import config
from .tokens_helper import AbstractTokensHelper


class RedisTokensHelper(AbstractTokensHelper):
    def __init__(self):
        self.redis = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_TOKEN_DB,
            decode_responses=True
        )
        self.token_set_name = config.REDIS_TOKEN_SET

    def token_exists(self, token: str) -> bool:
        """Проверка наличия токена в Redis"""
        return bool(self.redis.sismember(self.token_set_name, token))

    def add_token(self, token: str) -> None:
        """Добавление токена в Redis"""
        self.redis.sadd(self.token_set_name, token)

    def generate_and_save_token(self) -> str:
        """Генерация и сохранение нового токена"""
        token = secrets.token_urlsafe(32)
        self.add_token(token)
        return token

    def get_tokens(self) -> list[str]:
        """Получение списка всех токенов из Redis"""
        tokens = self.redis.smembers(self.token_set_name)
        return sorted(list(tokens))

    def delete_token(self, token: str) -> bool:
        """Удаление токена из Redis"""
        result = self.redis.srem(self.token_set_name, token)
        return result > 0
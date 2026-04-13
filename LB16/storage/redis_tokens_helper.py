import redis
import uuid


class RedisTokensHelper:
    """Класс для генерации и проверки токенов в Redis"""

    def __init__(self, redis_client=None):
        self.redis = redis_client or redis.Redis(host='localhost', port=6379, db=0)

    def generate_and_save_token(self):
        """Генерирует новый токен и сохраняет его в Redis"""
        token = str(uuid.uuid4())
        self.redis.set(token, "active", ex=3600)  # живет 1 час
        return token

    def token_exists(self, token):
        """Проверяет, существует ли токен в Redis"""
        return self.redis.exists(token) == 1
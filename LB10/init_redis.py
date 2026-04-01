import redis
import bcrypt
from core import config


def init_redis_data():
    """Инициализация тестовых данных в Redis"""

    # Подключаемся к Redis
    redis_client = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        decode_responses=True
    )

    # 1. Добавляем тестовые токены
    print("Добавление тестовых токенов...")
    token_redis = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_TOKEN_DB,
        decode_responses=True
    )

    # Старые токены из config.py
    old_tokens = [
        "bT5bs_OIUKZWwhCBc-y0yw",
        "tqL4D5U8wF41OHERP8i6gw",
    ]

    for token in old_tokens:
        token_redis.sadd(config.REDIS_TOKEN_SET, token)
        print(f"  Добавлен токен: {token}")

    # Добавляем новый тестовый токен
    new_token = "test_token_123"
    token_redis.sadd(config.REDIS_TOKEN_SET, new_token)
    print(f"  Добавлен токен: {new_token}")

    # 2. Добавляем тестовых пользователей
    print("\nДобавление тестовых пользователей...")
    user_redis = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_USER_DB,
        decode_responses=True
    )

    # Старые пользователи из config.py
    old_users = {
        "admin": "admin",
        "bob": "12345",
    }

    for username, password in old_users.items():
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        user_redis.set(f"user:{username}:password", hashed.decode('utf-8'))
        print(f"  Добавлен пользователь: {username}")

    # Добавляем нового тестового пользователя
    new_user = "alice"
    new_pass = "alice123"
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(new_pass.encode('utf-8'), salt)
    user_redis.set(f"user:{new_user}:password", hashed.decode('utf-8'))
    print(f"  Добавлен пользователь: {new_user}")

    # 3. Проверяем добавленные данные
    print("\nПроверка данных в Redis:")

    # Проверка токенов
    token_count = token_redis.scard(config.REDIS_TOKEN_SET)
    print(f"Токенов в базе: {token_count}")

    # Проверка пользователей
    user_keys = user_redis.keys("user:*:password")
    print(f"Пользователей в базе: {len(user_keys)}")
    for key in user_keys:
        username = key.split(":")[1]
        print(f"  - {username}")

    print("\nИнициализация данных завершена!")


if __name__ == "__main__":
    # Убедитесь, что Redis запущен
    try:
        init_redis_data()
    except redis.ConnectionError:
        print("Ошибка: Redis не запущен. Запустите Redis сервер.")
    except Exception as e:
        print(f"Ошибка при инициализации данных: {e}")
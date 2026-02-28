from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets


# Создаем объект безопасности
basic_security = HTTPBasic()


# Словарь пользователей (по заданию — в открытом виде)
users = {
    "admin": "1234",
    "user": "password"
}


def verify_basic_auth(
    credentials: HTTPBasicCredentials = Depends(basic_security)
):
    correct_password = users.get(credentials.username)

    if (
        correct_password is None or
        not secrets.compare_digest(credentials.password, correct_password)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username
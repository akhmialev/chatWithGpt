import jwt
from fastapi import Request
import hashlib
from datetime import timedelta, datetime

from fastapi.middleware.cors import CORSMiddleware
from db import check_db_max_count_ip
from config import SECRET_KEY, ALGORITHM


def add_middleware(app):
    """
        Функция для разрешения запросов с других доменов
    """
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def get_user_ip(request: Request):
    """
        Функция берет user id из request
    """
    client_ip = request.client.host
    if check_db_max_count_ip(client_ip):
        return True
    else:
        return False


def hash_password(password):
    """
        Функция для шифрования пароля.
    :param password: пароль
    """
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode('utf-8'))
    encrypted_password = sha256_hash.hexdigest()
    return encrypted_password


def create_access_token(data: dict, expire_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expire_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def check_token():
    ...
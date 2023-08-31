from fastapi import Request
import hashlib

from fastapi.middleware.cors import CORSMiddleware
from db import check_db_max_count_ip


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

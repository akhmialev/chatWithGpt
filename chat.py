from db import load_msg, save_msg, create_new_user, check_email
from tools import hash_password


def save_messages(request, msg, answer):
    """
        Функция для добавления в бд сообщений пользователя и ответов от ИИ.
    :param request: для получения IP пользователя.
    :param msg: сообщение пользователя.
    :param answer: ответ ИИ
    """
    client = request.client.host
    messages_to_add = [
        {'role': 'user', 'content': msg},
        {'role': 'assistant', 'content': answer}
    ]
    save_msg(client, messages_to_add)


def load_messages(request):
    """
        Функция для загрузки истории сообщений, что бы ИИ помнил историю.
    """
    client = request.client.host
    return load_msg(client)


def register(email, password):
    """
        Функция для регистрации пользователей
    :param email: почта
    :param password: пароль
    """
    password = hash_password(password)
    if check_email(email):
        return {'message': 'This email is already in use'}
    else:
        response = create_new_user(email, password)
        return response

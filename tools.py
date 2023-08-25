from fastapi import Request

from db import check_db_max_count_ip, load_msg, save_msg


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


def get_user_ip(request: Request):
    """
    Функция берет user id из request
    """
    client_ip = request.client.host
    if check_db_max_count_ip(client_ip):
        return True
    else:
        return False

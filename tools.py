import json
from fastapi import Request

from db import check_db_max_count_ip

messages = [
    {'role': 'system', 'content': 'Previous message'},
    {'role': 'user', 'content': ''}
]
ip_message_count = {}


def save_messages():
    with open('msg.json', 'w') as file:
        json.dump(messages, file)


def load_messages():
    global messages
    try:
        with open('msg.json', 'r') as file:
            messages = json.load(file)
    except FileNotFoundError:
        messages = []


def get_user_ip(request: Request):
    """
    Функция берет user id из request
    """
    client_ip = request.client.host
    if check_db_max_count_ip(client_ip):
        return True
    else:
        return False


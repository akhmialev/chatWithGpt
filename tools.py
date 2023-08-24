import json
from fastapi import Request

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
    client_ip = request.client.host
    return ip_message_count.get(client_ip, 0)

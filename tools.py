import json

messages = [
    {'role': 'system', 'content': 'Previous message'},
    {'role': 'user', 'content': ''}
]


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

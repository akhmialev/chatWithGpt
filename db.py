from datetime import datetime

from pymongo import MongoClient


def connect_to_db():
    """
    Функция подключения в бд
    """
    client = MongoClient('127.0.0.1', 27017)
    db = client['chat']
    return db


def check_db_max_count_ip(ip):
    """
    Функция проверяет есть ли юзер в базе и проверяет количество запросов не зарегистрированных пользователей(их 3)
    делает проверку даты(запросы можно задать 1 раз в сутки), в новых сутках чистит базу данных.
    :param ip: user ip
    """
    db = connect_to_db()
    today = datetime.today().date()
    collection = db.get_collection('users')
    query = {'ip': ip}
    user = collection.find_one(query)
    if user:
        if str(today) == str(user['date']):
            if int(user['count']) < 3:
                query = {'ip': ip}
                update_data = {'$set': {'count': user['count'] + 1}}
                collection.update_one(query, update=update_data)
                return False
            else:
                return True
        else:
            update_date = {"$set": {'count': 1, 'date': str(today), 'messages': []}}
            collection.update_one(query, update_date)
    else:
        data = {
            'ip': ip,
            'count': 1,
            'date': str(today),
            'messages': []
        }
        collection.insert_one(data)
        return False


def load_msg(ip):
    """
    Функция для загрузки истории сообщений.
    :param ip: IP пользователя
    """
    db = connect_to_db()
    collection = db.get_collection('users')
    query = {'ip': ip}
    user = collection.find_one(query)
    return user['messages']


def save_msg(ip, messages_to_add):
    """
    Функция для сохранения истории сообщений.
    :param ip: IP пользователя
    :param messages_to_add: сообщение пользователя и ответ ИИ для сохранения
    """
    db = connect_to_db()
    collection = db.get_collection('users')
    query = {'ip': ip}
    update_query = {"$push": {"messages": {"$each": messages_to_add}}}
    collection.update_one(query, update=update_query)


def create_new_user(email, password):
    db = connect_to_db()
    collection = db.get_collection('users')
    data = {
        'email': email,
        'password': password,
        'chat': [
            {
                'chat_name': '',
                'messages': []
            }
        ]
    }
    collection.insert_one(data)
    return True

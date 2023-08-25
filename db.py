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
            update_date = {"$set": {'count': 1, 'date': str(today)}}
            collection.update_one(query, update_date)
    else:
        data = {
            'ip': ip,
            'count': 1,
            'date': str(today)
        }
        collection.insert_one(data)
        return False

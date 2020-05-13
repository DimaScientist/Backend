from flask import Flask
from flask import abort
import time
from flask import jsonify
from flask import request
from flask import Response
import jwt
from bson.objectid import ObjectId
import pymongo

# везде выводить до 200 записи

app = Flask(__name__)
secretKey = "makeAmericaGreatAgain"
userTokenPassPattern = {'username': '', 'password_hash': '', 'time': 0}


def auth(request):
    """
    Функция, проверяющая наличие пользователя и срок годности
    токена
    :return: True - если найден пользователь, False - иначе
    """
    aut = str(request.headers['Authorization'])
    token = aut.split(' ')[1]
    obj = jwt.decode(token, secretKey, algorithms=['HS256'])
    prev_time_s = obj['time']
    prev_time = int(prev_time_s)
    curr_time = get_current_time()
    diff = curr_time - prev_time
    if diff > 2 * 60 * 60 * 1000:
        return False
    user = obj['username']
    password = obj['password_hash']
    users = get_db(get_connection())['users']
    found = users.find({'username': user})
    for user in found:
        if user['password_hash'] == password:
            return True
    return False


def auth_without_time_check(request):
    """
    Функция, проверяющая наличие
    пользователя по логину
    :param request: объект Flask
    :return: True - нашелся, False -  иначе
    """
    data = request.json
    user = data['user']
    password = data['pass']
    users = get_db(get_connection())['users']
    found = users.find({'username': user})
    for user in found:

        if user['password_hash'] == password:
            return True
    return False


def get_user(request):
    """
    :param request:
    :return:
    """
    data = request.json
    user = data['user']
    password = data['pass']
    users = get_db(get_connection())['users']
    found = users.find({'username': user})
    for user in found:
        if user['password_hash'] == password:
            return user


def get_connection():
    """
    Функция, создающая пользователя для управления
    базой данных
    :return: соединение с базой данных от имени данного пользователя
    """
    return pymongo.MongoClient(
        'mongodb://afanasiev_alexey:funny valentine did nothing wrong@140.82.36.93:27017/morning_wood')


def get_db(connection):
    """
    Функция, которая устанавливает соединение
    с MongoDB
    :param connection:
    :return: соединение с базой данных
    """
    return connection.get_database('morning_wood')


def get_current_time():

    return int(round(time.time() * 1000))


def search_lots(id_lots):

    conn = get_connection()
    db = get_db(conn)
    collection = db.get_collection('lots')
    res = []
    if id_lots == '':
        for lot in collection.find():
            temp = lot
            temp['_id'] = str(temp['_id'])
            res.append(temp)
    else:
        for lot in collection.find({'_id': ObjectId(id_lots)}):
            temp = lot
            temp['_id'] = str(temp['_id'])
            res.append(temp)
    return jsonify(res)


def show_all_lots():
    """
    Функция, выводящщая все товары
    :return: json-массив всех товаров
    """
    return search_lots('')


@app.route('/lots')
@app.route('/lots/<id_lot>')
def function_for_id_lots(id_lot=None):
    """
    Функция, выводящая товары по id
    :param id_lot: str, id товара
    :return: список товаров
    """
    re = auth(request)
    if re:
        if id_lot:
            return search_lots(id_lot)
        else:
            return show_all_lots()
    else:
        abort(401)


@app.route('/')
def hello():
    """
    Функция по умолчанию, показывающая
    установление связи с бекэндом
    :return: ответ бэкенда
    """
    return 'This is a backend server for project Morning Wood'


@app.route('/registration')
def register():

    data = request.json
    user = data['user']
    password = data['pass']
    bd = get_db(get_connection())
    collection = bd.get_collection('users')
    collection.insert({'username': user, 'password_hash': password})
    pattern = userTokenPassPattern
    pattern['username'] = user
    pattern['password_hash'] = password
    pattern['time'] = get_current_time()
    token = jwt.encode(pattern, secretKey, algorithm='HS256')
    resp = Response('success')
    resp.headers['Authorization'] = 'Bearer ' + (str(token, 'utf-8'))
    return resp


@app.route('/login')
def login():
    """
    Функция авторизации
    :return: Response, ответ на попытку авторизации
    """

    if (auth_without_time_check(request)):
        user = get_user(request)
        pattern = userTokenPassPattern
        pattern['username'] = user['username']
        pattern['password_hash'] = user['password_hash']
        pattern['time'] = get_current_time()
        token = jwt.encode(pattern, secretKey, algorithm='HS256')
        resp = Response('success')
        resp.headers['Authorization'] = 'Bearer ' + (str(token, 'utf-8'))
        return resp
    abort(401)


if __name__ == '__main__':
    app.run(debug=True)

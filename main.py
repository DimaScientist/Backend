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


def get_connection():
    return pymongo.MongoClient(
        'mongodb://afanasiev_alexey:funny valentine did nothing wrong@140.82.36.93:27017/morning_wood')


def get_db(connection):
    return connection.get_database('morning_wood')


def get_current_time():
    return int(round(time.time() * 1000))


def search_lots(id_lots):
    conn = get_connection()
    db = get_db(conn)
    collection = db.get_collection('lots')
    res = []
    if id_lots == '':
        print("empty id")
        for lot in collection.find():
            temp = lot
            temp['_id'] = str(temp['_id'])
            res.append(temp)
            print(temp)
    else:
        print("not empty id")
        for lot in collection.find({'_id': ObjectId(id_lots)}):
            temp = lot
            temp['_id'] = str(temp['_id'])
            res.append(temp)
            print(temp)
    return jsonify(res)


def show_all_lots():
    return search_lots('')


@app.route('/lots')
@app.route('/lots/<id_lot>')
def function_for_id_lots(id_lot=None):
    # если пусто получить все данные о лотах
    # если id, то вывести все лоты
    print(request.headers)
    auth = str(request.headers['Authorization'])
    token = auth.split(' ')[1]
    object = jwt.decode(token, secretKey, algorithms=['HS256'])
    prevTimeS = object['time']
    prevTime = int(prevTimeS)
    currtime = get_current_time()
    diff = currtime - prevTime
    if diff > 2 * 60 * 60 * 1000:
        abort(401)
        return
    user = object['username']
    password = object['password_hash']
    users = get_db(get_connection())['users']
    found = users.find({'username': user})
    for user in found:
        print(user)
        print(user['password_hash'])
        if user['password_hash'] == password:
            if id_lot:
                return search_lots(id_lot)
            else:
                return show_all_lots()
    abort(401)


@app.route('/')
def hello():
    return 'This is a backend server for project Morning Wood'


@app.route('/logout')
def delete_data_autif():
    # стирает данные о аутентификации
    pass


@app.route('/registration')
def register():
    data = request.json
    user = data['user']
    password = data['pass']
    print(data)
    print(user)
    print(password)
    bd = get_db(get_connection())
    collection = bd.get_collection('users')
    collection.insert({'username': user, 'password_hash': password})
    pattern = userTokenPassPattern
    pattern['username'] = user
    pattern['password_hash'] = password
    pattern['time'] = get_current_time()
    token = jwt.encode(pattern, secretKey, algorithm='HS256')
    object = jwt.decode(token, secretKey, algorithm='HS256')
    print(str(token, 'utf-8'))
    print(object)
    resp = Response('success')
    resp.headers['Authorization'] = 'Bearer ' + (str(token, 'utf-8'))
    return resp


@app.route('/login')
def login():
    return 'asd'


@app.route('/register')
def store_password():
    """
    POST /
      -- пароли уже провалидированы, не нужно сохранять сессию
      request: json { login: string, password: string, paswordConfirm: string }
      request: json { user: {login: string} }
      -> 201
    """
    pass


@app.route('/login')
def get_data_login():
    pass


print(__name__)
if __name__ == 'main':
    app.run(debug=True)

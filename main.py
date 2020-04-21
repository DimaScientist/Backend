from flask import Flask
from flask import jsonify
from bson.objectid import ObjectId
import pymongo

# везде выводить до 200 записи

app = Flask(__name__)


def get_connection():
    return pymongo.MongoClient(
        'mongodb://afanasiev_alexey:funny valentine did nothing wrong@140.82.36.93:27017/morning_wood')


def get_db(connection):
    return connection.get_database('morning_wood')


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
    if id_lot:
        return search_lots(id_lot)
    else:
        return show_all_lots()


@app.route('/')
def hello():
    return 'Hello world!!!'


@app.route('/logout')
def delete_data_autif():
    # стирает данные о аутентификации
    pass


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
    """
    request: json { login: string, password: string }
      response: json { user: {login: string}, token: string }
    """
    pass


@app.route('/mongo')
def testMongoConnection():
    conn = pymongo.MongoClient(
        'mongodb://afanasiev_alexey:funny valentine did nothing wrong@140.82.36.93:27017/morning_wood')
    name = conn.get_database().name
    conn.close()
    return name


print(__name__)
if __name__ == 'main':
    app.run(debug=True)

from flask import Flask

# везде выводить до 200 записи

app = Flask(__name__)


def search_lots(id_lots):
    pass


def show_all_lots():
    pass


@app.route('/lots')
@app.route('/lots/<id_lot>')
def function_for_id_lots(id_lots=None):
    # если пусто получить все данные о лотах
    # если id, то вывести все лоты
    if id_lots:
        return search_lots(id_lots)
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
    '''
    POST /
      -- пароли уже провалидированы, не нужно сохранять сессию
      request: json { login: string, password: string, paswordConfirm: string }
      request: json { user: {login: string} }
      -> 201
    '''


@app.route('/login')
def get_data_login():
    '''
    request: json { login: string, password: string }
      response: json { user: {login: string}, token: string }
    '''


if __name__ == 'main':
    app.run(debug=True)

from flask import Flask


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




if __name__ == 'main':
    app.run(debug=True)

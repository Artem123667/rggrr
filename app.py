from email import message

from flask import Flask, render_template, url_for, request, redirect, g, flash
import sys
import json
import sqlite3
import os
from FDataBase import FDataBase
from flask_flatpages import FlatPages, pygments_style_defs
import pathlib

script_path = pathlib.Path(sys.argv[0]).parent  # абсолютный путь до каталога, где лежит скрипт
conn = sqlite3.connect(script_path / "app.db")  # формируем абсолютный путь до файла базы

app = Flask(__name__)
DATABASE = '/kyrcovaz/app.db'
DEBUG = True
SECRET_KEY = 'dfgdgergerikjgbnkljghbefgvefvefvh'
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'app.db')))
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'
PORT_DIR = 'portfolio'
flatpages = FlatPages(app)


def connect_db():
    coon = sqlite3.connect(app.config['DATABASE'])
    coon.row_factory = sqlite3.Row
    return coon


def create_db():
    '''Функция для создания БД'''
    db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

    @app.teardown_appcontext
    def close_db(error):
        '''Закрытие соединения с БД, если оно было установленно'''
        if hasattr(g, 'link_db'):
            g.link_db.close()


def get_db():
    ''' Соединение с БД '''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db
    pass


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/portfolio')
def portfolio():
    return render_template("portfolio.html")

@app.route('/admin', methods=['POST', 'GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    if username == 'root' and password == 'pass':
        return render_template("login.html")

    return render_template("admin.html", message=message)

@app.route("/login")
def delPost():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('login.html', posts=dbase.delPost())

@app.route("/login", methods=["POST", "GET"])
def log():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('login.html', posts=dbase.getPostsAnonce())


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contacs')
def contacts():
    return render_template("/contacs.html")


@app.route('/resum')
def resum():
    return render_template("/resum.html")


@app.route("/contactsdb", methods=["POST", "GET"])
def addPost():
    with open('settings.txt', encoding='utf8') as config:
        data = config.read()
        settings = json.loads(data)
    tags = set()
    for p in flatpages:
        t = p.meta.get('tag')
        if t:
            tags.add(t.lower())
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['name']) > 2 and len(request.form['post']) > 2 and len(request.form['message']) > 2:
            res = dbase.addPost(request.form['name'], request.form['email'], request.form['post'],
                                request.form['message'])
            if not res:
                flash('  Ошибка добавления', category='error')
            else:

                flash('', category='success')
        else:
            flash('  Ошибка добавления', category='error')

    return render_template('contactsdb.html', bigheader=True, **settings, tags=tags)


if __name__ == "__main__":
    app.run(debug=True)
    # db = connect_db()
    create_db()

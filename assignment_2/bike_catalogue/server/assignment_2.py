import sqlite3
from flask import Flask, g
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import json

app = Flask(__name__, template_folder='../client/templates')
CORS(app)

DATABASE = 'bike_database.sqlite'


def parse_velostrana(db_conn):
    base_url = 'https://www.velostrana.ru'
    response = requests.get('https://www.velostrana.ru/shosseynye-velosipedy/shosseynye/')
    html_doc = response.content
    soup = BeautifulSoup(html_doc, 'html.parser')
    products = soup.find_all('div', class_='product__in')

    for product in products:
        model = product.find('span', class_='product__model').contents[0]
        price = product.find('p', class_='product__price-new').contents[0]
        img_link = product.find('img', class_='product__img-image')['src']
        add_entry(db_conn, model, price, base_url + img_link)


def parse_velopiter(db_conn):
    base_url = 'https://www.velopiter.ru'
    response = requests.get('https://www.velopiter.ru/fast/nedorogie-gorodskie-velosipedy/1.htm')
    html_doc = response.content
    soup = BeautifulSoup(html_doc, 'html.parser')
    products = soup.find_all('div', class_='proditem1')

    for product in products:
        model = product.find('div', class_='proditemtitle').find('a')['title']
        price = product.find('div', class_='price').find('span').contents[0]
        img_link = product.find('img')['src']
        add_entry(db_conn, model, price, base_url + img_link)


def get_db():
    db_conn = getattr(g, '_database', None)
    if db_conn is None:
        db_conn = g._database = sqlite3.connect(DATABASE)
    return db_conn


def add_entry(conn, model, price, img_link):
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT OR REPLACE INTO Bikes (model, price, img_link)
            VALUES (?, ?, ?)''',
        (model, price, img_link)
    )
    conn.commit()


@app.route('/')
def get_all():
    db_cursor = get_db().cursor()
    db_cursor.row_factory = sqlite3.Row
    db_cursor.execute('SELECT * From Bikes ORDER BY price ASC')
    bikes = db_cursor.fetchall()
    json_result = json.dumps([dict(row) for row in bikes])
    return json_result


def init_db():
    with app.app_context():
        db_conn = get_db()
        cursor = db_conn.cursor()
        cursor.executescript(
            '''CREATE TABLE IF NOT EXISTS Bikes
               (model text primary key, price integer not null, img_link string)'''
        )
        db_conn.commit()


def get_info():
    with app.app_context():
        conn = get_db()
        parse_velostrana(conn)
        parse_velopiter(conn)


@app.teardown_appcontext
def close_connection(exception):
    db_conn = getattr(g, '_database', None)
    if db_conn is not None:
        db_conn.close()


if __name__ == '__main__':
    init_db()
    get_info()
    app.run()

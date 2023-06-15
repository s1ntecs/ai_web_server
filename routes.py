from aiohttp import web
import aiohttp_jinja2
import jinja2
import sqlite3
import random
import json


async def index(request):
    headers = request.headers
    query = request.request.query_string
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO request (headers, query) VALUES (?, ?)", (headers, query))

    return aiohttp_jinja2.render_template('charakters.html', request, {})


async def get_data(request):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT headers, query FROM request")
    rows = c.fetchall()
    headers, query = zip(*rows)
    return aiohttp_jinja2.render_template('data.html', request,
                                          {'values': zip(headers, query)})


async def favorites(request):
    # Создание базы данных и подключение к ней
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Получение данных из таблицы characters
    c.execute("SELECT char_name, username, char_id FROM characters")
    # c.execute("SELECT char_name, username, char_id FROM characters WHERE username = 'sintecs")
    rows = c.fetchall()
    char_names, usernames, char_ids = zip(*rows)
    print(rows)
    # Закрытие соединения с базой данных
    conn.close()

    return aiohttp_jinja2.render_template('favorites.html', request,
                                          {'values': zip(char_names, usernames, char_ids)})


async def add_character(request):
    data = await request.json()
    name = data.get('name')
    username = data.get('username')
    char_id = data.get('char_id')
    # Создание базы данных и подключение к ней
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Вставка новой записи в таблицу
    c.execute("INSERT INTO characters (char_name, username, char_id) VALUES (?, ?, ?)", (name, username, char_id))
    conn.commit()

    # Закрытие соединения с базой данных
    conn.close()

    return web.Response(text='Character added successfully')

app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# Добавьте путь к папке со статическими файлами
app.router.add_static('/static/', path='static')

app.router.add_get('/', index)
app.router.add_get('/favorites', favorites)
app.router.add_post('/new_char', add_character)
app.router.add_post('/get_data', get_data)

web.run_app(app, host='0.0.0.0')

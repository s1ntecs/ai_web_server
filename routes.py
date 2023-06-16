from aiohttp import web
import urllib.parse

import aiohttp_jinja2
import jinja2
import sqlite3
import random
import json


async def index(request):
    # headers = str(request)
    # query = str(request.query)
    # conn = sqlite3.connect('database.db')
    # c = conn.cursor()
    # c.execute("INSERT INTO request (headers, query) VALUES (?, ?)", (headers, query))
    # conn.commit()

    # Закрытие соединения с базой данных
    # conn.close()
    return aiohttp_jinja2.render_template('charakters.html', request, {})


# async def get_data(request):
#     conn = sqlite3.connect('database.db')
#     c = conn.cursor()
#     c.execute("SELECT headers, query FROM request")
#     rows = c.fetchall()
#     headers, query = zip(*rows)
#     return aiohttp_jinja2.render_template('data.html', request,
#                                           {'values': zip(headers, query)})


async def favorites(request):
    user_id = urllib.parse.parse_qs(request.query_string).get('value', [None])[0]
    # Создание базы данных и подключение к ней
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    int_usr = int(user_id)
    # Получение данных из таблицы characters
    if user_id == "undefined":
        int_usr = 2
    c.execute("SELECT char_name, username, char_id FROM characters WHERE user_id = ?", (int_usr,))
    pers_chars = c.fetchall()
    pers_char_names, pers_usernames, pers_char_ids = zip(*pers_chars)

    c.execute("SELECT char_name, username, char_id FROM characters")
    all_chars = c.fetchall()
    char_names, usernames, char_ids = zip(*all_chars)
    # Закрытие соединения с базой данных
    conn.close()
    return aiohttp_jinja2.render_template('favorites.html', request=request,
                                      context={'values': zip(char_names, usernames, char_ids),
                                               'personal_values': zip(pers_char_names, pers_usernames, pers_char_ids)})

    # return aiohttp_jinja2.render_template('favorites.html', request,
    #                                       {'values': zip(char_names, usernames, char_ids)},
    #                                       {'personal_values': zip(pers_char_names, pers_usernames, pers_char_ids)})


async def add_character(request):
    data = await request.json()
    name = data.get('name')
    username = data.get('username')
    char_id = data.get('char_id')
    user_id = data.get('user_id')
    # Создание базы данных и подключение к ней
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Вставка новой записи в таблицу
    c.execute("INSERT INTO characters (char_name, username, user_id, char_id) VALUES (?, ?, ?, ?)", (name, username, user_id, char_id))
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
# app.router.add_get('/get_data', get_data)

web.run_app(app, host='0.0.0.0')

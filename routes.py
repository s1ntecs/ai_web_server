from aiohttp import web
import urllib.parse
import asyncpg
from const import main_chars_activity, url_list
import aiohttp_jinja2
import jinja2
import sqlite3

from analysis.actions import (amplitude_press_publick_bots_button,
                              amplitude_event_message,
                              amplitude_error,
                              amplitude_char_data_insert,
                              amplitude_get_char_data,
                              amplitude_site_loaded)
from scripts import refresh_counts, insert_data_main_chars

import asyncpg
import urllib.parse

async def get_connect():
    """ Создаем подключение к базе данных. """
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='postgres',
        password='susel'
    )
    return connection


async def index(request):
    user_id = urllib.parse.parse_qs(request.query_string).get('value', [None])[0]
    if user_id:
        event_name = "User press favorite_bots button"
        await amplitude_event_message(user_id, event_name)

    connection = await get_connect()

    try:
        # Получение данных из таблицы characters
        char_query = """
            SELECT char_name, username, char_id, actions_count
            FROM characters
            WHERE user_id = $1
        """
        all_chars = await connection.fetch(char_query, 7)
        char_names, usernames, char_ids, actions_count = zip(*all_chars)

    except Exception as e:
        if user_id:
            event_name = "Favorite Bots not found"
            await amplitude_error(user_id, event_name)
        char_names = usernames = char_ids = actions_count = []
        print(f"Error occurred: {e}")

    if user_id:
        event_name = "Favorite Bots tab data without self bots was been send to user"
        await amplitude_event_message(user_id, event_name)

    await connection.close()

    return aiohttp_jinja2.render_template(
        'charakters.html',
        request=request,
        context={'values': zip(
            char_names,
            usernames,
            char_ids,
            actions_count,
            main_chars_activity,
            url_list
        )}
    )


async def favorites(request):
    user_id = urllib.parse.parse_qs(request.query_string).get('value', [None])[0]

    # Создание базы данных и подключение к ней
    connection = await get_connect()

    try:
        # Получение данных из таблицы characters
        char_query = """
            SELECT char_name, username, char_id, actions_count
            FROM characters
            ORDER BY actions_count DESC
        """
        all_chars = await connection.fetch(char_query)
        char_names, usernames, char_ids, actions_count = zip(*all_chars)
    except Exception as e:
        event_name = "Community bots not found"
        await amplitude_error(user_id, event_name)
        char_names = usernames = char_ids = actions_count = []
        print(f"Error occurred: {e}")

    if user_id == "undefined":
        pers_char_names = pers_usernames = pers_char_ids = pers_actions_count = []
    else:
        int_usr = int(user_id)
        await amplitude_press_publick_bots_button(user_id)
        pers_char_query = """
            SELECT char_name, username, char_id, actions_count
            FROM characters
            WHERE user_id = $1
        """
        pers_chars = await connection.fetch(pers_char_query, int_usr)

        if not pers_chars:
            event_name = "Bots of community tab User did not have created bots"
            await amplitude_event_message(user_id, event_name)
            pers_char_names = pers_usernames = pers_char_ids = pers_actions_count = []
            event_name = "Bots of community tab data without self bots was been sent to user"
            await amplitude_event_message(user_id, event_name)

            return aiohttp_jinja2.render_template(
                'empty_favorites.html',
                request=request,
                context={
                    'values': zip(char_names, usernames, char_ids, actions_count),
                    'personal_values': zip(pers_char_names, pers_usernames, pers_char_ids, pers_actions_count)
                }
            )
        else:
            pers_char_names, pers_usernames, pers_char_ids, pers_actions_count = zip(*pers_chars)

    # Закрытие соединения с базой данных
    await connection.close()

    event_name = "Bots of community tab User had created bots"
    await amplitude_event_message(user_id, event_name)
    pers_char_names = pers_usernames = pers_char_ids = pers_actions_count = []
    event_name = "Bots of community tab Data with self bots was been sent to user"
    await amplitude_event_message(user_id, event_name)

    return aiohttp_jinja2.render_template(
        'favorites.html',
        request=request,
        context={
            'values': zip(char_names, usernames, char_ids, actions_count),
            'personal_values': zip(pers_char_names, pers_usernames, pers_char_ids, pers_actions_count)
        }
    )


async def all_bots(request):
    # Создаем подключение к базе данных
    connection = await get_connect()

    try:
        # Получение данных из таблицы characters
        char_query = """
            SELECT char_name, username, char_id
            FROM characters
        """
        all_chars = await connection.fetch(char_query)
        
        if not all_chars:
            char_names = usernames = char_ids = []
        else:
            char_names, usernames, char_ids = zip(*all_chars)
    except Exception as e:
        print(f"Error occurred: {e}")
        char_names = usernames = char_ids = []

    # Закрытие соединения с базой данных
    await connection.close()

    return aiohttp_jinja2.render_template(
        'bots_list.html',
        request=request,
        context={'values': zip(char_names, usernames, char_ids)}
    )


async def add_character(request):
    try:
        data = await request.json()
        name = data.get('name')
        username = data.get('username')
        char_id = data.get('char_id')
        user_id = data.get('user_id')
        await amplitude_get_char_data(user_id, char_id)

        # Создаем подключение к базе данных
        connection = await get_connect()

        # Вставка новой записи в таблицу
        insert_query = """
            INSERT INTO characters (char_name, username, user_id, char_id)
            VALUES ($1, $2, $3, $4)
        """
        await connection.execute(insert_query, name, username, user_id, char_id)

        # Закрытие соединения с базой данных
        await connection.close()
        await refresh_counts()
        await amplitude_char_data_insert(user_id, char_id)
        return web.Response(text='Character added successfully')
    except Exception as e:
        event_name = f"Web site backend created Bot data error: {e}"
        await amplitude_error(user_id, event_name)


async def site_loaded(request):
    user_id = urllib.parse.parse_qs(request.query_string).get('user_id', [None])[0]
    site_tab = urllib.parse.parse_qs(request.query_string).get('site_tab', [None])[0]
    bg_color = urllib.parse.parse_qs(request.query_string).get('bg_color', [None])[0]
    text_color = urllib.parse.parse_qs(request.query_string).get('text_color', [None])[0]
    hint_color = urllib.parse.parse_qs(request.query_string).get('hint_color', [None])[0]
    link_color = urllib.parse.parse_qs(request.query_string).get('link_color', [None])[0]
    button_color = urllib.parse.parse_qs(request.query_string).get('button_color', [None])[0]
    backgound_color = urllib.parse.parse_qs(request.query_string).get('backgound_color', [None])[0]
    event_name = "Web site is loaded"
    await amplitude_site_loaded(user_id,
                                event_name,
                                site_tab,
                                bg_color,
                                text_color,
                                hint_color,
                                link_color,
                                button_color,
                                backgound_color)
    return web.Response(text='to get requiest')


async def insert_main_chars_data(request):
    await insert_data_main_chars()
    return web.Response(text='Character added successfully')


async def delete_characters_table(request):
    # Подключение к базе данных
    conn = sqlite3.connect('sql3.db')
    c = conn.cursor()

    # Удаление таблицы "characters"
    c.execute("DROP TABLE IF EXISTS characters")

    # Сохранение изменений и закрытие соединения с базой данных
    conn.commit()
    conn.close()


app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# Добавьте путь к папке со статическими файлами
app.router.add_static('/static/', path='static')

app.router.add_get('/', index)
app.router.add_get('/all_chars', all_bots)
app.router.add_get('/favorites', favorites)
app.router.add_post('/new_char', add_character)
app.router.add_get('/del_bd', delete_characters_table)
app.router.add_get('/main_chars', insert_main_chars_data)
app.router.add_get('/site_loaded', site_loaded)

web.run_app(app, host='0.0.0.0')

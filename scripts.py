from aiohttp import web
import urllib.parse
import asyncpg

import aiohttp_jinja2
import jinja2
import sqlite3
import random
import json


async def get_connect():
    """ Создаем клавиатуру с функциями бота. """
    connection = await asyncpg.connect(host='65.108.53.155',
                                       port=5432,
                                       user='postgres',
                                       database='charactify',
                                       password='susel')
    return connection


async def refresh_counts():
    # Создание базы данных и подключение к ней
    conn = sqlite3.connect('sql3db.db')
    c = conn.cursor()
    connection_db = await get_connect()
    select_query = """
    SELECT character_id, count(*) from promts group by character_id
    """
    result = await connection_db.fetch(select_query)
    for row in result:
        print(row)
        char_id = row["char_id"]
        actions_count = row["count"]

        c.execute("UPDATE characters SET actions_count = ? WHERE char_id = ? ", (actions_count, char_id))
        conn.commit()
    conn.close()

import asyncpg
import asyncio

import sqlite3
from const import (welcome_msg_main_pers,
                   main_chars_name,
                   id_main_chars)


async def get_connect():
    """ Создаем клавиатуру с функциями бота. """
    connection = await asyncpg.connect(host='65.108.53.155',
                                       port=5432,
                                       user='postgres',
                                       database='charactify',
                                       password='susel')
    return connection


async def insert_data_main_chars():
    # Создание базы данных и подключение к ней
    conn = sqlite3.connect('sql3.db')
    c = conn.cursor()
    connection_db = await get_connect()
    insert_query = """
    INSERT INTO characters (char_id, name, welcome_msg) VALUES ($1, $2, $3)
    """
    user_id = 7
    username = "Admin"
    for i, char_name in enumerate(main_chars_name):
        char_id = id_main_chars[i]
        welcome_msg = welcome_msg_main_pers[i]
        await connection_db.execute(insert_query,
                                    char_id,
                                    char_name,
                                    welcome_msg)
        c.execute("INSERT INTO characters (char_name, username, user_id, char_id) VALUES (?, ?, ?, ?)", (
            char_name, username, user_id, char_id))
        conn.commit()
    conn.close()


async def main():
    await insert_data_main_chars()

# Создаем цикл событий (event loop)
loop = asyncio.get_event_loop()

# Запускаем асинхронную функцию
loop.run_until_complete(main())

# Завершаем цикл событий
loop.close()
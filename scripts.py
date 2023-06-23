import asyncpg

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


async def refresh_counts():
    # Создание базы данных и подключение к ней
    conn = sqlite3.connect('sql3.db')
    c = conn.cursor()
    connection_db = await get_connect()
    select_query = """
    SELECT character_id, count(*) from promts group by character_id
    """
    result = await connection_db.fetch(select_query)
    for row in result:
        char_id = row["character_id"]
        actions_count = row["count"]

        c.execute("UPDATE characters SET actions_count = ? WHERE char_id = ? ", (actions_count, char_id))
        conn.commit()
    conn.close()


async def insert_data_main_chars():
    # Создание базы данных и подключение к ней
    conn = sqlite3.connect('sql3.db')
    c = conn.cursor()
    connection_db = await get_connect()
    insert_query = """
    INSERT INTO characters (char_id, name, welcome_msg) VALUES ($1, $2, $3)
    ON CONFLICT (char_id, name, welcome_msg) DO NOTHING
    """
    user_id = 7
    username = "Admin"
    for i, char_name in enumerate(main_chars_name):
        char_id = id_main_chars[i]
        welcome_msg = welcome_msg_main_pers[i]
        try:
            await connection_db.execute(insert_query,
                                        char_id,
                                        char_name,
                                        welcome_msg)
        except Exception:
            pass
        c.execute("INSERT INTO characters (char_name, username, user_id, char_id) VALUES (?, ?, ?, ?)", (
            char_name, username, user_id, char_id))
        conn.commit()
    conn.close()

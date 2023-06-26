import asyncpg

import sqlite3
from const import (welcome_msg_main_pers,
                   main_chars_name,
                   id_main_chars)
from analysis.actions import amplitude_error


async def get_connect():
    """ Создаем клавиатуру с функциями бота. """
    connection = await asyncpg.connect(host='65.108.53.155',
                                       port=5432,
                                       user='postgres',
                                       database='charactify',
                                       password='susel')
    return connection


async def refresh_counts():
    # Создаем подключение к базе данных
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        password='susel',
        database='postgres'
    )

    try:
        select_query = """
            SELECT character_id, count(*) FROM promts GROUP BY character_id
        """
        result = await connection.fetch(select_query)

        for row in result:
            char_id = row["character_id"]
            actions_count = row["count"]

            update_query = """
                UPDATE characters SET actions_count = $1 WHERE char_id = $2
            """
            await connection.execute(update_query, actions_count, char_id)

    except Exception as e:
        print(f"Error occurred: {e}")

    # Закрываем подключение к базе данных
    await connection.close()


async def insert_data_main_chars():
    # Создание базы данных и подключение к ней
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        password='susel',
        database='postgres'
    )
    connection_db = await get_connect()
    my_db_query = """
    INSERT INTO characters (char_name, username, user_id, char_id)
     VALUES ($1, $2, $3, $4)"""
    insert_query = """
    INSERT INTO characters (char_id, name, welcome_msg) VALUES ($1, $2, $3)
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
        except Exception:  # В случае если уже имеется такой персонаж
            pass
        try:
            await connection.execute(my_db_query,
                                     char_name,
                                     username,
                                     user_id,
                                     char_id)
        except Exception:  # В случае если уже имеется такой персонаж
            pass

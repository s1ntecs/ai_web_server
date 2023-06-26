import asyncpg
import asyncio

CREATE_CHAR_TABLE = \
    '''CREATE TABLE IF NOT EXISTS characters
             (id SERIAL PRIMARY KEY,
             char_name TEXT,
             username TEXT,
             user_id INT,
             char_id INT,
             actions_count INT DEFAULT 0)'''


async def create_database():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='postgres',
                                       password='susel')
    print('sozdaetsya db product....')

    status = await connection.execute(CREATE_CHAR_TABLE)
    print(status)
    print('db sozdana')
    await connection.close()

asyncio.run(create_database())

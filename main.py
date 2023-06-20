from aiohttp import web
import aiohttp_jinja2
import jinja2
import sqlite3
from routes import index, add_character


# Создание базы данных и подключение к ней
conn = sqlite3.connect('sql3db.db')
c = conn.cursor()

# Создание таблицы в базе данных
c.execute('''CREATE TABLE IF NOT EXISTS characters
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             char_name TEXT,
             username TEXT,
             user_id INT,
             char_id INT)''')

c.execute('''CREATE TABLE IF NOT EXISTS request
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             headers TEXT,
             query TEXT)''')
# Закрытие соединения с базой данных
conn.close()

app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# Добавьте путь к папке со статическими файлами
app.router.add_static('/static/', path='static')

app.router.add_get('/', index)
app.router.add_post('/new_char', add_character)


web.run_app(app, host='0.0.0.0')

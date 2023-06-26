from aiohttp import web
import aiohttp_jinja2
import jinja2
from routes import index, add_character


# Создание базы данных и подключение к ней

app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# Добавьте путь к папке со статическими файлами
app.router.add_static('/static/', path='static')

app.router.add_get('/', index)
app.router.add_post('/new_char', add_character)


web.run_app(app, host='0.0.0.0')

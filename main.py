from aiohttp import web
import aiohttp_jinja2
import jinja2

async def index(request):
    return aiohttp_jinja2.render_template('charakters.html', request, {})

app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# Добавьте путь к папке со статическими файлами
app.router.add_static('/static/', path='static')

app.router.add_get('/', index)

web.run_app(app)

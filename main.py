from aiohttp import web
import aiohttp_jinja2
import jinja2

async def index(request):
    return aiohttp_jinja2.render_template('charakters.html', request, {})

async def echo(request):
    data = await request.json()
    return web.json_response(data)

app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# Добавьте путь к папке со статическими файлами
app.router.add_static('/static/', path='static')

app.router.add_get('/', index)
app.router.add_post('/hi', echo)  # Добавьте новый маршрут для эхо-ответа на /hi

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

from aiohttp import web
import logging
import redis

SET_NAME = 'numbers'

logging.basicConfig()

r = redis.Redis(host='redis', port=6379, db=0)

routes = web.RouteTableDef()


@routes.post('/increment')
async def handle(request: web.Request):
    number = await request.text()
    try:
        parsed_number = int(number, 10)
    except ValueError:
        logging.warning('number parsing error')
        return web.Response(body='number parsing error', status=400)

    if parsed_number < 0:
        logging.warning('number must be positive')
        return web.Response(body='number must be positive', status=400)

    if r.sismember(SET_NAME, number):
        logging.warning('number already exists')
        return web.Response(body='number already exists', status=400)

    incremented_number = f'{parsed_number + 1}'
    if r.sismember(SET_NAME, incremented_number):
        logging.warning('incremented number already exists')
        return web.Response(body='incremented number already exists', status=400)

    r.sadd(SET_NAME, parsed_number)

    return web.Response(body=incremented_number)


app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=8090)

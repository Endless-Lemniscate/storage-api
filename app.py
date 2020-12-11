from aiohttp import web
from routes import setup_routes
from aiohttp_swagger import *


if __name__ == "__main__":
    app = web.Application()
    setup_routes(app)
    setup_swagger(app, swagger_from_file="swagger.yaml")
    web.run_app(app, host='localhost', port=8080)

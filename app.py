from routes import setup_routes
from aiohttp_swagger import *
from aiohttp import web
import yaml


cfg = yaml.full_load(open("config.yaml", "r"))

if __name__ == "__main__":
    app = web.Application()
    setup_routes(app)
    setup_swagger(app, swagger_from_file=cfg.get('path_to_swagger'))
    web.run_app(app, host=cfg.get('host'), port=cfg.get('port'))

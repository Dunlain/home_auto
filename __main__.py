from wsgiref.simple_server import make_server

import settings
from core.routes import create_routes as create_core_routes


if __name__ == '__main__':
    config = settings.create_configuration()
    # Register views for requests to server
    create_core_routes(config)
    # Create WSGI App
    app = config.make_wsgi_app()
    # Launch server
    server = make_server(settings.SERVER_HOST[0], settings.SERVER_HOST[1], app)
    server.serve_forever()
# Stack Packages
from wsgiref.simple_server import make_server
# Home Automation Packages
import settings


if __name__ == '__main__':
    config = settings.create_configuration()
    # Create WSGI App
    app = config.make_wsgi_app()
    # Launch server
    server = make_server(settings.SERVER_HOST[0], settings.SERVER_HOST[1], app)
    server.serve_forever()
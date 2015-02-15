import pyramid_jinja2

from pyramid.config import Configurator
from pyramid.response import Response
from wsgiref.simple_server import make_server

from core.routes import create_routes as create_core_routes


def hello_world(request):
    return Response('Hello {name:s}!'.format(name=request.matchdict['name']))

if __name__ == '__main__':
    config = Configurator()
    config.add_static_view('static', 'static/', cache_max_age=3600)
    config.include(pyramid_jinja2)
    config.add_renderer('.html', factory=pyramid_jinja2.renderer_factory)
    # Register views for requests to server
    create_core_routes(config)
    # Create WSGI App
    app = config.make_wsgi_app()
    # Launch server
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
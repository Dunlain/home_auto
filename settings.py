import pyramid_jinja2
from pyramid.config import Configurator

SERVER_HOST = ('0.0.0.0', 8080)


def create_configuration():
    config = Configurator()
    config.add_static_view('static', 'static/', cache_max_age=3600)
    config.include(pyramid_jinja2)
    config.add_renderer('.html', factory=pyramid_jinja2.renderer_factory)
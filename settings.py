# Stack Packages
import pyramid_jinja2
from pyramid.config import Configurator
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
# Home Automation Packages
import core.routes

# Default Server Hosts
SERVER_HOST = ('0.0.0.0', 8080)
DB_HOST = ('0.0.0.0', 5432)

# Default Database Settings
DB_SETTINGS = {

}

# Server Default Template Renderer
TEMPLATE_RENDERER = pyramid_jinja2

# Rate at which templates are refreshed (seconds)
MAX_CACHE_AGE = 3600

# View modules
VIEW_ROUTERS = (
    core.routes,  # Core views
)


def db_factory(request):
    """
    Create a database session upon a successful request to the home automation server.
    This allows an SQLAlchemy session to be available in view code as ``request.db`` or ``config.registry.dbmaker()``.

    :param request: an HTTP request object
    :return: a database session
    """
    maker = request.registry.dbmaker
    session = maker()

    def cleanup(request):
        if request.exception is not None:
            session.rollback()
        else:
            session.commit()
        session.close()
    request.add_finished_callback(cleanup)

    return session


def create_configuration():
    """
    Create the app configuration based upon the settings.py file
    :return: The app Configurator object.
    """
    config = Configurator()

    # Add Database Engine
    engine = create_engine(DB_HOST, DB_SETTINGS)
    config.registry.dbmaker = sessionmaker(bind=engine)
    config.add_request_method(db_factory, reify=True)

    # Add Static Files
    config.add_static_view('static', 'static/', cache_max_age=MAX_CACHE_AGE)

    # Add Template Renderer
    config.include(TEMPLATE_RENDERER)
    config.add_renderer('.html', factory=TEMPLATE_RENDERER.renderer_factory)

    # Register views for requests to server
    for router_module in VIEW_ROUTERS:
        router_module.create_routes(config)

    return config
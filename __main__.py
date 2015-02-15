# Stack Packages
from pyramid.config import Configurator
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from wsgiref.simple_server import make_server
# Home Automation Packages
import settings


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
    db_url = "{backend}://{user}:{password}@{host}/{database}".format(
        backend="+".join(settings.DB_BACKEND),
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=":".join(settings.DB_HOST),
        database=settings.DB_NAME
    )
    engine = create_engine(db_url, **settings.DB_SETTINGS)
    config.registry.dbmaker = sessionmaker(bind=engine)
    config.add_request_method(db_factory, reify=True)

    # Add Static Files
    config.add_static_view('static', 'static/', cache_max_age=settings.MAX_CACHE_AGE)

    # Add Template Renderer
    config.include(settings.TEMPLATE_RENDERER)
    config.add_renderer('.html', factory=settings.TEMPLATE_RENDERER.renderer_factory)

    # Register views for requests to server
    for router_module in settings.VIEW_ROUTERS:
        router_module.create_routes(config)

    return config


if __name__ == '__main__':
    config = create_configuration()
    # Create WSGI App
    app = config.make_wsgi_app()
    # Launch server
    server = make_server(settings.SERVER_HOST[0], settings.SERVER_HOST[1], app)
    server.serve_forever()
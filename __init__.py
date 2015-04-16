# Stack Packages
from pyramid.config import Configurator
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from wsgiref.simple_server import make_server
# Home Automation Packages
from core.models import Base
import settings


def db_factory(request):
    """
    Create a database session upon a successful request to the home automation server.
    This allows an SQLAlchemy session to be available in view code as ``request.db`` or ``config.registry.dbmaker()``.

    :param request: an HTTP request object
    :return: a database session
    """
    session = request.registry.dbmaker()

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
    config = Configurator(settings=settings.APP_SETTINGS)
    for renderer_name, factory in settings.APP_RENDERERS:
        config.add_renderer(renderer_name, factory)

    # Register views for requests to server
    for package_views in settings.REGISTERED_PACKAGES:
        for view, patterns in package_views.items():
            for route_name, route_pattern in patterns.items():
                print("Adding routes \"{}\" for \"{}\"".format(route_name, route_pattern))
                config.add_route(route_name, route_pattern)
                config.add_view(view, route_name=route_name)

    # Register static files to server
    for static_view_name, path in settings.STATIC_FILES:
        config.add_static_view(static_view_name, path, cache_max_age=settings.MAX_CACHE_AGE)

    # Add Database Engine
    db_url = "{backend}://{user}:{password}@{host}/{database}".format(
        backend=settings.DB_BACKEND,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST if isinstance(settings.DB_HOST, str) else "{0:s}:{1:d}".format(*settings.DB_HOST),
        database=settings.DB_NAME
    )
    engine = create_engine(db_url, **settings.DB_SETTINGS)
    # Create all tables defined in core.models in the database
    Base.metadata.create_all(engine)
    config.registry.dbmaker = sessionmaker(bind=engine)
    config.add_request_method(db_factory, reify=True)

    return config


if __name__ == '__main__':
    configuration = create_configuration()
    # Create WSGI App
    app = configuration.make_wsgi_app()
    # Launch server
    server = make_server(settings.SERVER_HOST[0], settings.SERVER_HOST[1], app)
    server.serve_forever()
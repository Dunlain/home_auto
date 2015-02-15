from pyramid.config import Configurator
from .views import LoginView


def create_routes(config: Configurator):
    config.add_route(LoginView.route_name, LoginView.pattern)
    config.add_view(LoginView, route_name=LoginView.route_name)
from pyramid.config import Configurator
from .views import LoginView, HomeView


def create_routes(config: Configurator):
    # Login Page
    config.add_route(LoginView.route_name, LoginView.pattern)
    config.add_view(LoginView, route_name=LoginView.route_name)
    # Home Page
    config.add_route(HomeView.route_name, HomeView.pattern)
    config.add_view(HomeView, route_name=HomeView.route_name)
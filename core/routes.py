"""
This module is used to help the Configurator generate view routes.
To "activate" a view/route simply add the View to the "route" tuple.
Each view MUST have a pattern and route_name attribute.
    EG:
    registered_views: {
        MyView: {
            'name1': 'pattern1',
            ...
        },
        YourView: {
            ...
        }
        ...
    }
"""
from .views import LoginView, HomeView, ListView, StuffView


registered_views = {
    # Home Page
    HomeView: {
        'home': '',
        'home1': '/'
    },
    # Login Page
    LoginView: {
        'login': 'login',
        'user_login': 'login/{username}'
    },
    # List Page
    ListView: {
        'lists': 'lists',
    },
    # Stuff Page
    StuffView: {
        'stuff': 'stuff',
    }
}
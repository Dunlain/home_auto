# Stack Packages
import pyramid_jinja2
# Home Automation Packages
from core.routes import registered_views as core_views


# In Debug Mode Flag
DEV = True

# Default Server Hosts
SERVER_HOST = ('localhost', 8080)
DB_HOST = ('localhost', 5432)

# Default Database backend and driver
DB_BACKEND = 'postgresql'

# Default database username and password
DB_USER = ''
DB_PASSWORD = ''

# Default database name
DB_NAME = 'home_auto_dev'

# Rate at which templates are refreshed (seconds)
MAX_CACHE_AGE = 3600

# Default Pyramid App Settings
APP_SETTINGS = {
    'pyramid.reload_templates': DEV,  # If in Debug Mode reload templates from disk
    'pyramid.includes': [
        'pyramid_jinja2',             # Add Template Renderer
    ],
    # Adding Jinja2 Filters
    'jinja2.filters': {
        'model_url': 'pyramid_jinja2.filters:model_url_filter',
        'route_url': 'pyramid_jinja2.filters:route_url_filter',
        'static_url': 'pyramid_jinja2.filters:static_url_filter',
    }
}

APP_RENDERERS = (
    ('.jinja2', pyramid_jinja2.renderer_factory),
    ('.html', pyramid_jinja2.renderer_factory),
)

# Default Database Settings
DB_SETTINGS = {

}

# View modules
#  - To include a new package's routes the routes module must be added here
REGISTERED_PACKAGES = (
    core_views,  # Core views
)

# Static file directories
# - To include new static files, such as css, js or images list the name and file path
STATIC_FILES = (
    ('static', 'static/'),
)
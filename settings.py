# Stack Packages
import pyramid_jinja2
# Home Automation Packages
import core.routes


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
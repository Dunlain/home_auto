# Stack Packages
from pyramid.httpexceptions import HTTPMethodNotAllowed, HTTPFound, HTTPNotFound, HTTPUnauthorized, HTTPBadRequest, \
    HTTPServerError
from pyramid.renderers import render
from pyramid.response import Response
from pyramid.request import Request

from sqlalchemy.orm.exc import NoResultFound

# Home Automation Packages
from core.models import Base, List, ListCategory
from .models import User


class BaseView(object):
    """
    Delegates HTTP requests to View objects methods.
        HTTP GET -> self.get
        HTTP POST -> self.post
        HTTP PUT -> self.put
        HTTP DELETE -> self.delete
    """
    template = None

    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.db_session = request.registry.dbmaker()

    def __call__(self):
        method = self.request.method.lower()
        try:
            response_func = getattr(self, method)

        except AttributeError as err:
            raise HTTPMethodNotAllowed("HTTP {} is not supported.".format(method.upper())) from err
        else:
            # If a POST request was made check the CSRF token
            if method.lower() == "post":
                token = self.request.session.get_csrf_token()
                if token != self.request.POST.get('csrf_token'):
                    raise HTTPServerError("CSRF Token does not match.")

            response = response_func()

        return response

    def render(self, template_dict: dict):
        try:
            template_dict['csrf_token'] = self.request.session.get_csrf_token()
            response = Response(render(self.template, template_dict, request=self.request))

        except (ValueError, AttributeError) as err:
            raise HTTPServerError("View improperly configured.") from err
        else:
            return response

    def get_or_create(self, model: Base, **kwargs):
        """
        Get a model from the database or, if it doesn't exist, create it.
        """
        try:
            model_instance = self.db_session.query(model).filter_by(**kwargs)
        except NoResultFound:
            model_instance = model(**kwargs)
            self.db_session.add(model_instance)

        return model_instance

    def get_or_404(self, model: Base, **kwargs):
        """
        Get a model from the database or, if it doesn't exist, raise an HTTP 404 Exception.
        """
        try:
            model_instance = self.db_session.query(model).filter_by(**kwargs)
        except NoResultFound as err:
            raise HTTPNotFound() from err

        return model_instance


class HomeView(BaseView):
    """
    Directs to login page, dependent upon HTTP request type
    """
    template = 'core:templates/home.html'

    def get(self):
        return self.render({})

    def post(self):
        post = self.request.POST
        try:
            user_name = post['name']
            user_email = post['email']
            user_pwd = post['password']

        except KeyError:
            response = HTTPFound(self.request.route_url('home'))

        else:
            new_user = User(name=user_name, email=user_email, password=user_pwd)
            self.db_session.add(new_user)
            response = HTTPFound(self.request.route_url('home'))

        return Response(response)


class LoginView(BaseView):
    """
    Directs to login page, dependent upon HTTP request type
    """
    template = 'core:templates/login.html'

    def get(self):
        return self.render({})

    def post(self):
        post = self.request.POST
        try:
            username = post['username']
            password = post['password']
            try:
                user = self.db_session.query(User).filter_by(name=username, password=password)
            except NoResultFound as err:
                error = "The User with the name {} and password does not exist".format(username, password)
                raise HTTPUnauthorized(error) from err

        except KeyError:
            pass  # TODO: Notify the user that they omitted login info

        response = HTTPFound(self.request.route_url('login'))

        return response


class ListView(BaseView):
    """
    Directs to lists page, dependent upon HTTP request type
    """
    template = 'core:templates/lists.html'

    def get(self):
        categories = self.db_session.query(ListCategory).all()
        template_dict = {
            'categories': categories,
        }

        return self.render(template_dict)

    def post(self):
        # TODO: Create everything needed in a real post
        return Response("I've been posted!")


class StuffView(BaseView):
    """
    Directs to Stuff page, dependent up HTTP request type
    """
    template = 'core:templates/stuff.html'

    def get(self):
        return self.render({})

    def post(self):
        # TODO: Create everything needed in a real post
        return Response("I've been posted!")
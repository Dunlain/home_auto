# Stack Packages
from pyramid.httpexceptions import HTTPMethodNotAllowed, HTTPFound
from pyramid.renderers import render
from pyramid.response import Response
# Home Automation Packages
from .models import User


class BaseView(object):
    """
    Delegates HTTP requests to View objects methods.
        HTTP GET -> self.get
        HTTP POST -> self.post
        HTTP PUT -> self.put
        HTTP DELETE -> self.delete
    """
    def __init__(self, request):
        self.request = request

    def __call__(self):
        method = self.request.method.lower()
        try:
            response_func = getattr(self, method)
            response = response_func()

        except AttributeError:
            response = HTTPMethodNotAllowed()

        return response


class HomeView(BaseView):
    """
    Directs to login page, dependent upon HTTP request type
    """
    def get(self):
        render_template = render('core:templates/home.html', {}, request=self.request)
        return Response(render_template)

    def post(self):
        post = self.request.POST
        try:
            user_name = post['name']
            user_email = post['email']
            user_pwd = post['password']

        except KeyError:
            response = HTTPFound(self.request.route_url('home'))

        else:
            session = self.request.db
            new_user = User(name=user_name, email=user_email, password=user_pwd)
            session.add(new_user)

            response = HTTPFound(self.request.route_url('home'))

        return Response(response)


class LoginView(BaseView):
    """
    Directs to login page, dependent upon HTTP request type
    """
    def get(self):
        render_template = render('core:templates/login.html', {}, request=self.request)
        return Response(render_template)

    def post(self):
        # TODO: Create everything needed in a real post
        return Response("I've been posted!")


class ListView(BaseView):
    """
    Directs to lists page, dependent upon HTTP request type
    """
    def get(self):
        render_template = render('core:templates/lists.html', {}, request=self.request)
        return Response(render_template)

    def post(self):
        # TODO: Create everything needed in a real post
        return Response("I've been posted!")


class StuffView(BaseView):
    """
    Directs to Stuff page, dependent up HTTP request type
    """
    def get(self):
        render_template = render('core:templates/stuff.html', {}, request=self.request)
        return Response(render_template)

    def post(self):
        # TODO: Create everything needed in a real post
        return Response("I've been posted!")
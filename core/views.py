from pyramid.httpexceptions import HTTPMethodNotAllowed
from pyramid.renderers import render
from pyramid.response import Response


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
from pyramid.httpexceptions import HTTPMethodNotAllowed
from pyramid.renderers import render
from pyramid.response import Response


class LoginView(object):
    """
    Directs to login page, dependent upon HTTP request type
    """
    route_name = 'login'
    pattern = 'login/{id}'

    def __init__(self, request):
        self.request = request

    def __call__(self):
        if self.request.method == 'GET':
            return self.get()
        elif self.request.method == 'POST':
            return self.post()
        else:
            return HTTPMethodNotAllowed()

    def get(self):
        # TODO: Create actual get method for... get
        render_template = render('core:templates/login.html', {}, request=self.request)
        return Response(render_template)

    def post(self):
        # TODO: Create everything needed in a real post
        return Response("I've been posted!")
import unittest
from pyramid import testing
from .routes import create_routes


class CoreTest(unittest.TestCase):
    """
    Base class for core view tests.
    """
    def setUp(self):
        self.config = testing.setUp()
        create_routes(self.config)

    def tearDown(self):
        testing.tearDown()


class LoginTest(CoreTest):
    """
    Testing the login view.
    """
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_get(self):
        request = testing.DummyRequest()


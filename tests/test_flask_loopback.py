import socket
from contextlib import contextmanager

import flask
import flask_loopback
import requests
from flask_loopback import dispatch
from flask_loopback._compat import httplib
from urlobject import URLObject as URL

from . import TestCase
from flask_loopback.flask_loopback import CustomHTTPResponse

OK_RESPONSE = "ok!"
_g_counter = 0

def create_sample_app():
    returned = flask.Flask(__name__)

    @returned.route("/sample/url")
    def sample_view():
        return OK_RESPONSE

    @returned.route("/increase_counter")
    def increase_counter():
        global _g_counter
        _g_counter += 1
        return flask.jsonify({"result": _g_counter})

    @returned.route('/remote_addr')
    def get_remote_addr():
        return flask.jsonify({'result': flask.request.remote_addr})

    l = flask_loopback.FlaskLoopback(returned)

    return returned, l

class FlaskLoopbackActivationTest(TestCase):

    def setUp(self):
        super(FlaskLoopbackActivationTest, self).setUp()
        self.app, self.loopback = create_sample_app()
        self.assertFalse(dispatch._registered_addresses)
        self.loopback.activate_address(("a.com", 123))
        self.loopback.activate_address(("b.com", 1234))

    def test_deactivate_one_by_one(self):
        self.assertEquals(len(dispatch._registered_addresses), 2)
        self.loopback.deactivate_address(("a.com", 123))
        self.assertEquals(len(dispatch._registered_addresses), 1)
        with self.assertRaises(LookupError):
            self.loopback.deactivate_address(("a.com", 123))
        self.loopback.deactivate_address(("b.com", 1234))
        self.assertFalse(dispatch._registered_addresses)

    def test_deactivate_all(self):
        self.loopback.deactivate_all()
        self.assertFalse(dispatch._registered_addresses)

class FlaskLoopbackTest(TestCase):

    def setUp(self):
        super(FlaskLoopbackTest, self).setUp()
        self.app, self.loopback = create_sample_app()
        self.address = ("somehost.com", 1234)
        self.root_url = _url(self.address)
        self._ctx = self.loopback.on(self.address)
        ctx_result = self._ctx.__enter__()
        self.addCleanup(self._ctx.__exit__, None, None, None)

    def test_simple_request(self):
        self.assertEquals(requests.get(self.root_url.add_path("/sample/url")).content.decode("utf-8"), OK_RESPONSE)

    def test_response_attributes(self):
        url = self.root_url
        response = requests.get(url)
        self.assertEquals(response.url, url)
        self.assertEquals(response.request.url, url)
        self.assertEquals(response.request.method, "GET")

    def test_remote_addr(self):
        response = requests.get(self.root_url.add_path('remote_addr'))
        response.raise_for_status()
        assert response.json()['result'] == socket.getfqdn()

    def test_not_found(self):
        response = requests.get(self.root_url.add_path("not_found"))
        self.assertEquals(response.status_code, httplib.NOT_FOUND)
        self.assertEquals(response.reason, "Not Found")

    def test_request_context_handler(self):
        initial_counter = _g_counter

        @self.loopback.register_request_context_handler
        @contextmanager
        def increase_counter(request):
            global _g_counter
            _g_counter += 1
            yield
            _g_counter += 1

        returned = requests.get(self.root_url.add_path("increase_counter")).json()["result"]
        self.assertEquals(_g_counter, initial_counter + 3)
        self.assertEquals(returned, initial_counter + 2)

    def test_request_context_handler_custom_response(self):
        initial_counter = _g_counter

        @self.loopback.register_request_context_handler
        @contextmanager
        def return_custom_code(request):
            raise CustomHTTPResponse(request, 666)

        response = requests.get(self.root_url.add_path("increase_counter"))
        assert response.status_code == 666
        self.assertEquals(_g_counter, initial_counter)
        self.assertIsNone(response.content)


def _url(address):
    return URL("http://{0}:{1}/".format(*address))

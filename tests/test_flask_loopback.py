from flask_loopback._compat import httplib

import flask
import flask_loopback
import requests
from urlobject import URLObject as URL

from . import TestCase

OK_RESPONSE = "ok!"

def create_sample_app():
    returned = flask.Flask(__name__)

    @returned.route("/sample/url")
    def sample_view():
        return OK_RESPONSE

    l = flask_loopback.FlaskLoopback(returned)

    return returned, l


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
        self.assertEquals(requests.get(self.root_url.add_path("/sample/url")).content, OK_RESPONSE)

    def test_not_found(self):
        response = requests.get(self.root_url.add_path("not_found"))
        self.assertEquals(response.status_code, httplib.NOT_FOUND)

def _url(address):
    return URL("http://{0}:{1}/".format(*address))

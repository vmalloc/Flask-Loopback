import gzip
import hashlib

import pytest
from flask import Flask, g, jsonify, request, Response
from flask_loopback import FlaskLoopback
from urlobject import URLObject as URL


@pytest.fixture
def active_app(request, app, ssl_port, non_ssl_port, hostname):
    app.activate_address((hostname, ssl_port), ssl=True)
    app.activate_address((hostname, non_ssl_port), ssl=False)
    @request.addfinalizer
    def cleanup():
        app.deactivate_address((hostname, ssl_port))
        app.deactivate_address((hostname, non_ssl_port))

@pytest.fixture
def app():
    returned = Flask(__name__)

    @returned.route("/echo", methods=["post"])
    def echo():                 # pylint: disable=unused-variable
        return jsonify({
            "result": True,
            })

    @returned.route('/request_vars')
    def get_request_vars():     # pylint: disable=unused-variable
        return jsonify(dict(
            (name, getattr(request, name))
            for name in ['host']))


    @returned.route('/set_cookie')
    def set_cookie():           # pylint: disable=unused-variable
        returned = jsonify({})
        returned.set_cookie('x', value='y')
        return returned

    @returned.route('/assert_no_cookies')
    def assert_no_cookies():    # pylint: disable=unused-variable
        assert not request.cookies
        return jsonify({"result": "ok"})


    @returned.route('/set_cookie_on_after_request')
    def set_cookie_on_after_request(): # pylint: disable=unused-variable
        g.cookies.append(('x', 'y'))
        return jsonify({})

    @returned.route('/stream_upload', methods=['POST'])
    def stream_upload():        # pylint: disable=unused-variable
        return hashlib.sha512(request.stream.read()).hexdigest()

    @returned.route('/compressed')
    def compressed():        # pylint: disable=unused-variable
        orig = 'uncompressed!'.encode('utf-8')
        return Response(gzip.compress(orig), headers={'Content-Encoding': 'gzip'})


    @returned.before_request
    def before():
        g.cookies = []

    @returned.after_request
    def after_request(response):
        cookies = getattr(g, 'cookies', [])
        while cookies:
            response.set_cookie(*cookies.pop())

        return response


    return FlaskLoopback(returned)

@pytest.fixture
def ssl_port():
    return 10443

@pytest.fixture
def non_ssl_port():
    return 10080

@pytest.fixture
def hostname():
    return "some-nonexistant-hostname.localdomain"

@pytest.fixture(params=[True, False])
def url(request, hostname, ssl_port, non_ssl_port):
    with_ssl = request.param

    return URL('http{0}://{1}:{2}'.format('s' if with_ssl else '', hostname, ssl_port if with_ssl else non_ssl_port))

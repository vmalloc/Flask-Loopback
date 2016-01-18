from flask import Flask, jsonify, request
from flask_loopback import FlaskLoopback

import pytest

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
    def echo():
        return jsonify({
            "result": True,
            })

    @returned.route('/request_vars')
    def get_request_vars():
        return jsonify(dict(
            (name, getattr(request, name))
            for name in ['host']))


    @returned.route('/set_cookie')
    def set_cookie():
        returned = jsonify({})
        returned.set_cookie('x', value='y')
        return returned

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

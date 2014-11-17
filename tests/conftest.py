from flask import Flask, jsonify
from flask_loopback import FlaskLoopback

import pytest


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


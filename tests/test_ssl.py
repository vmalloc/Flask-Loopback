import ssl

import requests

import pytest


def test_ssl_fails_for_non_ssl_port(active_app, hostname, ssl_port, non_ssl_port):
    with pytest.raises(ssl.SSLError):
        requests.get("https://{0}:{1}".format(hostname, non_ssl_port))

def test_non_ssl_fails_for_ssl_port(active_app, hostname, ssl_port, non_ssl_port):
    with pytest.raises(requests.ConnectionError):
        requests.get("http://{0}:{1}".format(hostname, ssl_port))


import ssl
import requests
import pytest


@pytest.mark.usefixtures('active_app', 'ssl_port')
def test_ssl_fails_for_non_ssl_port(hostname, non_ssl_port):
    with pytest.raises(ssl.SSLError):
        requests.get("https://{0}:{1}".format(hostname, non_ssl_port))


@pytest.mark.usefixtures('active_app', 'non_ssl_port')
def test_non_ssl_fails_for_ssl_port(hostname, ssl_port):
    with pytest.raises(requests.ConnectionError):
        requests.get("http://{0}:{1}".format(hostname, ssl_port))

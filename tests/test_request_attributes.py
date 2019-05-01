import pytest
import requests


@pytest.mark.usefixtures('active_app')
def test_request_host(url):
    assert requests.get(url.add_path('request_vars')).json()['host'] == url.netloc

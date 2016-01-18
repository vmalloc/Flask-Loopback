# pylint: disable=unused-argument
import pytest
import requests


@pytest.mark.parametrize('path', ['set_cookie', 'set_cookie_on_after_request'])
def test_cookies(active_app, url, path):
    resp = requests.get(url.add_path(path))
    assert resp.cookies['x'] == 'y'

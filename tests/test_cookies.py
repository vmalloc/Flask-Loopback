# pylint: disable=unused-argument
import pytest
import requests


@pytest.mark.parametrize('path', ['set_cookie', 'set_cookie_on_after_request'])
@pytest.mark.parametrize('with_session', [True, False])
def test_cookies(active_app, url, path, with_session):
    url = url.add_path(path)
    if with_session:
        session = requests.Session()
        resp = session.get(url)
    else:
        resp = requests.get(url)
    assert resp.cookies['x'] == 'y'
    if with_session:
        assert session.cookies['x'] == 'y'

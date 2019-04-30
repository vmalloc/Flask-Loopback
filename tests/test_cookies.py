# pylint: disable=unused-argument
import pytest
import requests


@pytest.mark.parametrize('path', ['set_cookie', 'set_cookie_on_after_request'])
@pytest.mark.parametrize('with_session', [True, False])
def test_cookies(active_app, url, path, with_session, cookie_name, cookie_value):
    url = url.add_path(path)
    if with_session:
        session = requests.Session()
        resp = session.get(url)
    else:
        resp = requests.get(url)
    resp.raise_for_status()
    assert resp.cookies[cookie_name] == cookie_value
    if with_session:
        assert session.cookies[cookie_name] == cookie_value


def test_client_forgets_cookies(active_app, url):
    resp = requests.get(url.add_path('set_cookie'))
    resp.raise_for_status()

    requests.get(url.add_path('assert_no_cookies')).raise_for_status()


def test_client_session_remembers_cookies(active_app, url):
    s = requests.Session()
    s.get(url.add_path('set_cookie'))
    s.get(url.add_path('assert_cookies')).raise_for_status()

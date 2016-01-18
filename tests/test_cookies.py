import requests


def test_cookies(active_app, url):
    resp = requests.get(url.add_path('set_cookie'))
    assert resp.cookies['x'] == 'y'

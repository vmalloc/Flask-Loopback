import requests

def test_request_host(active_app, url):
    assert requests.get(url.add_path('request_vars')).json()['host'] == url.netloc

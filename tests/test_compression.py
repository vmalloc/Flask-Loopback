import requests


def test_compression(active_app, url): # pylint: disable=unused-argument

    resp = requests.get(url.add_path('compressed'))
    resp.raise_for_status()
    assert resp.content.decode('utf-8') == 'uncompressed!'

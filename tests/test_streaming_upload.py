import hashlib

import requests


def test_streaming_upload(active_app, url, tmpdir): # pylint: disable=unused-argument
    data = ("this is a data" * 400).encode('utf-8')
    h = hashlib.sha512(data).hexdigest()

    tmp_path = tmpdir.join('datafile')
    with tmp_path.open('wb') as f:
        f.write(data)

    with tmp_path.open('rb') as f:
        resp = requests.post(url.add_path('stream_upload'), data=f)

    resp.raise_for_status()
    assert resp.content.decode('utf-8') == h

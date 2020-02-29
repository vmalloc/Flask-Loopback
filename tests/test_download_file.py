import os

import pytest
import requests


def read_response_using_iter_content(resp):
    return b''.join([chunk for chunk in resp.iter_content(chunk_size=1024)])


def read_response_using_content(resp):
    return resp.content


@pytest.mark.parametrize("read_response", [read_response_using_content, read_response_using_iter_content])
@pytest.mark.parametrize("file_type", ["binary", "text"])
def test_download_file(active_app, url, read_response, file_type):  # pylint: disable=unused-argument
    resp = requests.get(url.add_path("files").add_path(file_type))
    resp.raise_for_status()
    result = read_response(resp)
    with open(os.path.join(os.path.dirname(__file__), 'files', file_type), 'rb') as f:
        assert result == f.read()

import requests
from contextlib import contextmanager

from . import dispatch
from ._compat import iteritems


class FlaskLoopback(object):

    def __init__(self, flask_app):
        super(FlaskLoopback, self).__init__()
        self.flask_app = flask_app
        self._test_client = flask_app.test_client()

    @contextmanager
    def on(self, address):
        dispatch.register_loopback_handler(address, self)
        try:
            yield self
        finally:
            dispatch.unregister_loopback_handler(address)

    def handle_request(self, url, request):
        assert url.scheme
        path = "/{0}".format(url.split("/", 3)[-1])
        open_kwargs = {"method": request.method.upper(), "headers": iteritems(request.headers), "data": request.body}
        resp = self._test_client.open(path, **open_kwargs)
        returned = requests.Response()
        returned.status_code = resp.status_code
        returned._content = resp.get_data()
        returned.headers.update(resp.headers)
        return returned


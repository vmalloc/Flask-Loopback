import requests
from contextlib import contextmanager
try:
    from contextlib import ExitStack
except ImportError:
    from contextlib2 import ExitStack

from . import dispatch
from ._compat import iteritems


class FlaskLoopback(object):

    def __init__(self, flask_app):
        super(FlaskLoopback, self).__init__()
        self.flask_app = flask_app
        self._test_client = flask_app.test_client()
        self._request_context_handlers = []
        self._registered_addresses = set()

    def register_request_context_handler(self, handler):
        self._request_context_handlers.append(handler)

    @contextmanager
    def on(self, address):
        self.activate_address(address)
        try:
            yield self
        finally:
            self.deactivate_address(address)

    def activate_address(self, address):
        dispatch.register_loopback_handler(address, self)
        self._registered_addresses.add(address)

    def deactivate_address(self, address):
        dispatch.unregister_loopback_handler(address)
        self._registered_addresses.remove(address)

    def deactivate_all(self):
        while self._registered_addresses:
            self.deactivate_address(next(iter(self._registered_addresses)))

    def handle_request(self, url, request):
        assert url.scheme
        path = "/{0}".format(url.split("/", 3)[-1])
        open_kwargs = {"method": request.method.upper(), "headers": iteritems(request.headers), "data": request.body}
        with ExitStack() as stack:
            for handler in self._request_context_handlers:
                stack.enter_context(handler(request))

            resp = self._test_client.open(path, **open_kwargs)
            returned = requests.Response()
            returned.status_code = resp.status_code
            returned._content = resp.get_data()
            returned.headers.update(resp.headers)
            return returned

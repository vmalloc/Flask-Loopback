import requests
try:
    from ssl import SSLError
except ImportError:
    SSLError = None
from urlobject import URLObject as URL

_registered_addresses = {}

def register_loopback_handler(address, handler, ssl):
    _registered_addresses[address] = (handler, ssl)
    _patch_requests_if_needed()

def unregister_loopback_handler(address):
    _registered_addresses.pop(address)
    _unpatch_requests_if_no_longer_needed()

def _fake_requests_send(self, request, **kwargs):
    url = URL(request.url)

    address = (url.hostname, url.port or url.default_port)

    handler, ssl = _registered_addresses.get(address, (None, None))

    if handler is None:
        return _orig_session_send(self, request, **kwargs)

    request_is_ssl = url.scheme == "https"
    if request_is_ssl and not ssl:
        if SSLError is None:
            raise NotImplementedError() # pragma: no cover
        raise SSLError()
    if not request_is_ssl and ssl:
        raise requests.ConnectionError()

    return handler.handle_request(self, url, request)

_requests_patched = False
_orig_session_send = None

def _patch_requests_if_needed():
    global _orig_session_send
    global _requests_patched

    if _requests_patched:
        return

    assert _registered_addresses
    _orig_session_send = requests.sessions.Session.send
    requests.sessions.Session.send = _fake_requests_send
    _requests_patched = True

def _unpatch_requests_if_no_longer_needed():
    global _orig_session_send
    global _requests_patched

    if not _requests_patched or _registered_addresses:
        return

    assert _orig_session_send
    requests.sessions.Session.send = _orig_session_send
    _orig_session_send = None
    _requests_patched = False

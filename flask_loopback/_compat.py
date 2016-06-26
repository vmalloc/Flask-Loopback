from contextlib import contextmanager
import gzip
import sys

PY2 = sys.version_info < (3, 0)

if PY2:
    iteritems = lambda d: d.iteritems() # not dict.iteritems!!! we support ordered dicts as well
else:
    iteritems = lambda d: iter(d.items()) # not dict.items!!! See above

if PY2:
    from cStringIO import StringIO as BytesIO
    import httplib

else:
    from io import BytesIO
    import http.client as httplib


def gzip_compress(data):
    s = BytesIO()
    with gzip.GzipFile(fileobj=s, mode='wb') as f:
        f.write(data)

    return s.getvalue()

def gzip_decompress(data):
    s = BytesIO(data)
    with gzip.GzipFile(fileobj=s, mode='rb') as f:
        return f.read()

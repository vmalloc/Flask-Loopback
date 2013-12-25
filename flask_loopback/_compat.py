import sys

PY2 = sys.version_info < (3, 0)

if PY2:
    iteritems = lambda d: d.iteritems() # not dict.iteritems!!! we support ordered dicts as well
else:
    iteritems = lambda d: iter(d.items()) # not dict.items!!! See above

if PY2:
    import httplib
else:
    import http.client as httplib

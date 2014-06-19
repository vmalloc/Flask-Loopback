![Build Status] (https://secure.travis-ci.org/vmalloc/Flask-Loopback.png ) &nbsp; ![Downloads] (https://pypip.in/d/Flask-Loopback/badge.png ) &nbsp; ![Version] (https://pypip.in/v/Flask-Loopback/badge.png )

Overview
========

Flask-Loopback enables you to use written Flask applications in your code to mock actual web services. This is useful if you are writing a client that will use an existing web service and would like to know how well it will interact with the real thing.

Flask-Loopback does this without actually sending HTTP requests over the network, but rather through stubbing the `requests` package so that only requests directed at your mock will arrive at their destination.

Doing this is very simple. You probably already have a flask application somewhere that you'd like to use

```python
# myapp.py
>>> import flask

>>> app = flask.Flask(__name__)

>>> @app.route("/some/path")
... def hello():
...     return "hello!"

```

When you want to actually use it, you activate the loopback on a specified address:

```python
>>> import requests
>>> from flask.ext.loopback import FlaskLoopback

>>> loopback = FlaskLoopback(app)

>>> with loopback.on(("some-address.com", 80)):
...    print(requests.get("http://some-address.com/some/path").content.decode("utf-8"))
hello!

```

To help you perform more actions before and after requests, you can register request context functions to be called around actual requests (this is in addition to the default handlers provided by Flask):

```python
>>> from contextlib import contextmanager

>>> @loopback.register_request_context_handler
... @contextmanager
... def request_handler(request):
...     # do something before request handling
...     yield
...     # do something after request handling

```

SSL
===

SSL is disabled by default, but you can easily activate it:

```python
>>> with loopback.on(("some-address.localdomain", 443)):
...    requests.get("https://some-address.localdomain/some/path") # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
	...
SSLError
>>> with loopback.on(("some-address.localdomain", 443), ssl=True):
...    requests.get("https://some-address.localdomain/some/path") # doctest: +IGNORE_EXCEPTION_DETAIL
<Response [200]>

```



Licence
=======

BSD3 (See `LICENSE`)


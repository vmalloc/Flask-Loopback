import os
import sys
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "flask_loopback", "__version__.py")) as version_file:
    exec(version_file.read()) # pylint: disable=W0122

_INSTALL_REQUIERS = [
    "requests",
    "Flask",
    "URLObject",
]

if sys.version_info < (2, 7):
    _INSTALL_REQUIERS.append("unittest2")

if sys.version_info < (3, 3):
    _INSTALL_REQUIERS.append("contextlib2")

setup(name="Flask-Loopback",
      classifiers = [
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.3",
          ],
      description="Library for faking HTTP requests using flask applications without actual network operations",
      license="BSD3",
      author="Rotem Yaari",
      author_email="vmalloc@gmail.com",
      version=__version__, # pylint: disable=E0602
      packages=find_packages(exclude=["tests"]),

      url="https://github.com/vmalloc/flask-loopback",

      install_requires=_INSTALL_REQUIERS,
      scripts=[],
      namespace_packages=[]
      )

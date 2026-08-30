"""Route fork matching HTTP HEAD method."""

from pyresponse.fork.method import Method


class Head(Method):
    """Route fork matching HTTP HEAD method."""

    METHOD = "HEAD"

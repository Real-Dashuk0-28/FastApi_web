import unittest

from dependencies import USAFE_METHODS


class TestUnsafeMethods:

    def test_unsafe_methods_doesnt_contain_dafe_methods():
        safe_methods = {"GET", "HEAD", "OPTIONS"}
        assert USAFE_METHOD & safe_methods == set()

    def test_all_method_are_upper(self):
        assert all(method.isupper() for method in USAFE_METHODS)

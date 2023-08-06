# pylint: skip-file
import unittest

from unimatrix.ext import webapi


class SubresourceTestCase(unittest.TestCase):

    class parent(webapi.Endpoint):
        resource_name = 'foo'

        class child(webapi.Endpoint):
            resource_name = 'bar'

        subresources = [child]

    def test_qualname_returns_proper_path_parent(self):
        endpoint = self.parent(None)
        self.assertEqual(endpoint.qualname, 'foo')

    def test_qualname_returns_proper_path(self):
        endpoint = self.parent.child(None)
        self.assertEqual(endpoint.qualname, 'foo.bar')

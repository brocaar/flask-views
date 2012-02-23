import unittest2 as unittest

from flask import Flask


class BaseTestCase(unittest.TestCase):
    """
    Base test-case class.
    """
    def setUp(self):
        self.app = Flask(__name__)
        self.app.debug = True
        self.client = self.app.test_client()

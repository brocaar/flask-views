import json

from flask import url_for

from flask_views.json import JSONView
from flask_views.tests.functional.base import BaseTestCase


class JSONViewTestCase(BaseTestCase):
    """
    Tests for :py:class:`.JSONView`.
    """
    def setUp(self):
        super(JSONViewTestCase, self).setUp()

        class TestView(JSONView):
            pass

        self.app.add_url_rule(
            '/test/<user>/',
            view_func=TestView.as_view('test')
        )

    def test_get(self):
        """
        Test GET request.
        """
        with self.app.test_request_context():
            response = self.client.get(url_for('test', user='foo'))
        self.assertEqual(200, response.status_code)

        self.assertEqual({
            'params': {
                'user': 'foo',
            }
        }, json.loads(response.data))

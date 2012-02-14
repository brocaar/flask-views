from flask import url_for

from flask_views.base import View, TemplateView
from flask_views.tests.functional.base import BaseTestCase


class ViewTestCase(BaseTestCase):
    """
    Tests for :py:class:`.View`.
    """
    def setUp(self):
        super(ViewTestCase, self).setUp()

        class TestView(View):
            def get(self, *args, **kwargs):
                return 'GET: {0}'.format(kwargs.get('user'))

            def post(self, *args, **kwargs):
                return 'POST: {0}'.format(kwargs.get('user'))

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
        self.assertEqual('GET: foo', response.data)

    def test_post(self):
        """
        Test POST request.
        """
        with self.app.test_request_context():
            response = self.client.post(url_for('test', user='bar'))
        self.assertEqual(200, response.status_code)
        self.assertEqual('POST: bar', response.data)


class TemplateViewTestCase(BaseTestCase):
    """
    Tests for :py:class:`.TemplateView`.
    """
    def setUp(self):
        super(TemplateViewTestCase, self).setUp()

        class TestView(TemplateView):
            template_name = 'template_view.html'

        self.app.add_url_rule(
            '/test/<user>/',
            view_func=TestView.as_view('test'),
        )

    def test_get(self):
        """
        Test GET request.
        """
        with self.app.test_request_context():
            response = self.client.get(url_for('test', user='foo'))
        self.assertEqual(200, response.status_code)
        self.assertEqual('User: foo', response.data)

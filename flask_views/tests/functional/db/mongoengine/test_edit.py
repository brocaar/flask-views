from flask import url_for

from flask_views.db.mongoengine.edit import CreateView
from flask_views.tests.functional.db.mongoengine.base import BaseMongoTestCase


class CreateViewTestCase(BaseMongoTestCase):
    """
    Tests for :py:class:`.CreateView`.
    """
    def setUp(self):
        super(CreateViewTestCase, self).setUp()

        class TestView(CreateView):
            model = self.TestDocument
            form_class = self.TestForm
            template_name = 'model_form_view.html'
            success_url = 'http://google.com/'

        self.app.add_url_rule('/test/', view_func=TestView.as_view('test'))

    def test_get(self):
        """
        Test GET request.
        """
        self.assertEqual(0, self.TestDocument.objects.count())

        with self.app.test_request_context():
            response = self.client.get(url_for('test'))
        self.assertEqual(200, response.status_code)
        self.assertIn('name="username"', response.data)
        self.assertIn('name="name"', response.data)
        self.assertEqual(0, self.TestDocument.objects.count())

    def test_empty_post(self):
        """
        Test empty POST request.
        """
        self.assertEqual(0, self.TestDocument.objects.count())

        with self.app.test_request_context():
            response = self.client.post(url_for('test'))
        self.assertEqual(200, response.status_code)
        self.assertIn('name="username"', response.data)
        self.assertIn('name="name"', response.data)
        self.assertEqual(0, self.TestDocument.objects.count())

    def test_post(self):
        """
        Test POST request with valid data.
        """
        self.assertEqual(0, self.TestDocument.objects.count())

        with self.app.test_request_context():
            response = self.client.post(url_for('test'), data={
                'username': 'foo',
                'name': 'bar',
            })
        self.assertEqual(302, response.status_code)
        self.assertEqual('http://google.com/', response.headers['Location'])
        self.assertEqual(1, self.TestDocument.objects.count())

        self.TestDocument.objects.get(username='foo', name='bar')

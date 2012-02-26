from flask import url_for

from flask_views.db.mongoengine.edit import CreateView, UpdateView
from flask_views.tests.functional.db.mongoengine.base import BaseMongoTestCase


class CreateViewTestCase(BaseMongoTestCase):
    """
    Tests for :py:class:`.CreateView`.
    """
    def setUp(self):
        super(CreateViewTestCase, self).setUp()

        class TestView(CreateView):
            document_class = self.TestDocument
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


class UpdateViewTestCase(BaseMongoTestCase):
    """
    Tests for :py:class:`.UpdateView`.
    """
    def setUp(self):
        super(UpdateViewTestCase, self).setUp()

        class TestView(UpdateView):
            document_class = self.TestDocument
            form_class = self.TestForm
            template_name = 'model_form_view.html'
            success_url = 'http://google.com/'
            get_fields = {
                'username': 'user',
            }

        self.app.add_url_rule('/<user>/', view_func=TestView.as_view('test'))

        test_obj = self.TestDocument(username='foo', name='bar')
        test_obj.save()

    def test_get(self):
        """
        Test GET request.
        """
        with self.app.test_request_context():
            response = self.client.get(url_for('test', user='foo'))
        self.assertEqual(200, response.status_code)
        self.assertIn('value="foo"', response.data)
        self.assertIn('value="bar"', response.data)

    def test_post(self):
        """
        Test POST request with valid data.
        """
        with self.app.test_request_context():
            response = self.client.post(url_for('test', user='foo'), data={
                'username': 'john',
                'name': 'Foo Bar',
            })
        self.assertEqual(302, response.status_code)
        self.assertEqual('http://google.com/', response.headers['Location'])
        self.assertEqual(1, self.TestDocument.objects.count())

        self.TestDocument.objects.get(username='john', name='Foo Bar')

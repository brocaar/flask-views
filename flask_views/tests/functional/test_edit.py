from flask import url_for
from wtforms import fields, validators
from wtforms.form import Form

from flask_views.edit import FormView
from flask_views.tests.functional.base import BaseTestCase


class FormViewTestCase(BaseTestCase):
    """
    Test for :py:class:`.FormView`.
    """
    def setUp(self):
        super(FormViewTestCase, self).setUp()

        class TestForm(Form):
            username = fields.TextField('Username', [validators.required()])

        class TestView(FormView):
            form_class = TestForm
            template_name = 'form_view.html'
            success_url = 'http://google.com/'
            initial = {
                'username': 'Foo',
            }

        self.app.add_url_rule('/form/', view_func=TestView.as_view('test'))

    def test_get(self):
        """
        Test GET request.
        """
        with self.app.test_request_context():
            response = self.client.get(url_for('test'))
        self.assertEqual(200, response.status_code)
        self.assertIn('name="username"', response.data)
        self.assertIn('value="Foo"', response.data)

    def test_empty_post(self):
        """
        Test empty POST request.
        """
        with self.app.test_request_context():
            response = self.client.post(url_for('test'), data={
                'username': '',
            })
        self.assertEqual(200, response.status_code)
        self.assertIn('name="username"', response.data)

    def test_post_data(self):
        """
        Test POST request with valid data.
        """
        with self.app.test_request_context():
            response = self.client.post(url_for('test'), data={
                'username': 'Foo',
            })
        self.assertEqual(302, response.status_code)
        self.assertEqual('http://google.com/', response.headers['Location'])

from flask import url_for

from flask_views.db.mongoengine.detail import DetailView
from flask_views.tests.functional.db.mongoengine.base import BaseMongoTestCase


class DetailTestCase(BaseMongoTestCase):
    """
    Tests for :py:class:`.DetailView`.
    """
    def setUp(self):
        super(DetailTestCase, self).setUp()

        class TestView(DetailView):
            document_class = self.TestDocument
            get_fields = {
                'username': 'user',
            }
            template_name = 'detail_template.html'

        self.app.add_url_rule('/<user>/', view_func=TestView.as_view('test'))

    def test_get(self):
        """
        Test GET request.
        """
        test_obj = self.TestDocument(username='foo', name='bar')
        test_obj.save()

        with self.app.test_request_context():
            response = self.client.get(url_for('test', user='foo'))
        self.assertEqual(200, response.status_code)
        self.assertEqual('bar', response.data)

    def test_get_404(self):
        """
        Test GET request with 404 response.
        """
        with self.app.test_request_context():
            response = self.client.get(url_for('test', user='foo'))
        self.assertEqual(404, response.status_code)

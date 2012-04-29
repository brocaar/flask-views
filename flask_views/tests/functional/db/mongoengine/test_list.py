from flask import url_for

from flask_views.db.mongoengine.list import ListView
from flask_views.tests.functional.db.mongoengine.base import BaseMongoTestCase


class ListViewTestCase(BaseMongoTestCase):
    """
    Tests for :py:class:`.ListView`.
    """
    def setUp(self):
        super(ListViewTestCase, self).setUp()

        test_obj = self.TestDocument(
                name='foofoo',
                username='user',
            )
        test_obj.save()

        for i in range(1, 12):
            test_obj = self.TestDocument(
                name='testtest',
                username='user{0}'.format(i)
            )
            test_obj.save()

        class TestView(ListView):
            document_class = self.TestDocument
            filter_fields = {
                'name': 'name',
            }
            template_name = 'list_template.html'
            items_per_page = 3

        self.app.add_url_rule(
            '/<name>/<int:page>/',
            view_func=TestView.as_view('test')
        )

    def test_get_pages(self):
        """
        Test GET requests for pages 1 - 4.
        """
        for i in range(1, 5):
            with self.app.test_request_context():
                response = self.client.get(
                    url_for('test', name='testtest', page=i))

                self.assertEqual(200, response.status_code)

    def test_get_404(self):
        """
        Test GET request resulting in 404.
        """
        with self.app.test_request_context():
            response = self.client.get(
                url_for('test', name='testtest', page=5))

        self.assertEqual(404, response.status_code)

    def test_template_context(self):
        """
        Test template context variables.
        """
        with self.app.test_request_context():
            response = self.client.get(
                url_for('test', name='testtest', page=4))

        self.assertTrue('Is paginated: True' in response.data)
        self.assertTrue('Users: user10, user11' in response.data)
        self.assertTrue('Current page: 4' in response.data)
        self.assertTrue('Total page count: 4' in response.data)

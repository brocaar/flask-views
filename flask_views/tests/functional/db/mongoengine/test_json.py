import json

from flask import url_for
from mongoengine import fields
from mongoengine.document import EmbeddedDocument

from flask_views.db.mongoengine.json import JSONDetailView
from flask_views.tests.functional.db.mongoengine.base import BaseMongoTestCase


class JSONDetailViewTestCase(BaseMongoTestCase):
    """
    Tests for :py:class:`.JSONDetailView`.
    """
    def setUp(self):
        super(JSONDetailViewTestCase, self).setUp()

        class TestEmbeddedDocument(EmbeddedDocument):
            body = fields.StringField(required=True)
        self.TestEmbeddedDocument = TestEmbeddedDocument

    def setup_test_view(self, document):
        class TestView(JSONDetailView):
            document_class = document
            get_fields = {
                'username': 'user',
            }
        self.app.add_url_rule('/<user>/', view_func=TestView.as_view('test'))

    def test_basic(self):
        """
        Basic test for JSON encoding.
        """
        self.setup_test_view(self.TestDocument)
        test_obj = self.TestDocument(username='foo', name='bar')
        test_obj.save()

        with self.app.test_request_context():
            response = self.client.get(url_for('test', user='foo'))
        self.assertEqual({
            'username': 'foo',
            'name': 'bar',
            'id': unicode(test_obj.id),
        }, json.loads(response.data))

    def test_embedded_document_list(self):
        """
        Test with embedded document.
        """
        class TestDocument(self.TestDocument):
            embedded_doc = fields.EmbeddedDocumentField(
                self.TestEmbeddedDocument)

        self.setup_test_view(TestDocument)

        test_obj = TestDocument(
            username='foo',
            name='bar',
            embedded_doc=self.TestEmbeddedDocument(body='embedded1'),
        )
        test_obj.save()

        with self.app.test_request_context():
            response = self.client.get(url_for('test', user='foo'))
        self.assertEqual({
            'id': unicode(test_obj.id),
            'username': 'foo',
            'name': 'bar',
            'embedded_doc': {'body': 'embedded1'},
        }, json.loads(response.data))

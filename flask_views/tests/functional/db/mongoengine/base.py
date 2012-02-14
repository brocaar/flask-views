from mongoengine import connect, fields
from mongoengine.document import Document

from flask_views.tests.functional.base import BaseTestCase


class BaseMongoTestCase(BaseTestCase):
    """
    Base test-case class for MongoDB tests.
    """
    def setUp(self):
        super(BaseMongoTestCase, self).setUp()

        self.db = connect('brocaar_flask_views_test')

        class TestDocument(Document):
            username = fields.StringField(
                verbose_name='Username',
                required=True,
            )
            name = fields.StringField(
                verbose_name='Name',
                required=True,
            )

        self.TestDocument = TestDocument

    def tearDown(self):
        for collection in self.db.collection_names():
            if collection.split('.')[0] != 'system':
                self.db.drop_collection(collection)

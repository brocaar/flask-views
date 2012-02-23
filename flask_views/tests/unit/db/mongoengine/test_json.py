import unittest2 as unittest

from mock import patch, Mock

from flask_views.db.mongoengine.json import (
    MongoengineEncoder, JSONDetailView, JSONResponseMixin)


class MongoengineEncoderTestCase(unittest.TestCase):
    """
    Tests for :py:class:`.MongoengineEncoder`.
    """
    def test_default_iter(self):
        """
        Test :py:meth:`.MongoengineEncoder.default` with iterable.
        """
        class DummyIter(dict):
            def __getattr__(self, name):
                return self[name]

        encoder = MongoengineEncoder()
        dummy_iter = DummyIter({'foo': 'bar'})
        self.assertEqual({'foo': 'bar'}, encoder.default(dummy_iter))

    @patch('flask_views.db.mongoengine.json.ObjectId', Mock)
    def test_default_object_id(self):
        """
        Test :py:meth:`.MongoengineEncoder.default` ``ObjectId`` object.
        """
        obj = Mock()
        encoder = MongoengineEncoder()
        self.assertEqual(unicode(obj), encoder.default(obj))

    @patch('flask_views.db.mongoengine.json.json')
    def test_default_default_fallback(self, json):
        """
        Test :py:meth:`.MongoengineEncoder.default` with default fallback.
        """
        json.JSONEncoder.default.return_value = 'default-fallback'

        obj = Mock()
        encoder = MongoengineEncoder()
        self.assertEqual('default-fallback', encoder.default(obj))
        json.JSONEncoder.default.assert_called_once_with(encoder, obj)


class JSONResponseMixinTestCase(unittest.TestCase):
    """
    Tests for :py:class:`.JSONResponseMixin`.
    """
    def test_encoder_class(self):
        """
        Test :py:attr:`.JSONResponseMixin.encoder_class`.
        """
        mixin = JSONResponseMixin()
        self.assertEqual(MongoengineEncoder, mixin.encoder_class)


class JSONDetailViewTestCase(unittest.TestCase):
    """
    Tests for :py:class:`.JSONDetailView`.
    """
    def test_get_context_data(self):
        """
        Test :py:meth:`.JSONDetailView.get_context_data`.
        """
        view = JSONDetailView()
        view.object = Mock()
        self.assertEqual(view.object, view.get_context_data())

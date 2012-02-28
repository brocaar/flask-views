import unittest2 as unittest

from mock import Mock

from flask_views.db.mongoengine.list import MultipleObjectMixin


class MultipleObjectMixinTestCase(unittest.TestCase):
    """
    Tests for :py:class:`.MultipleObjectMixin`.
    """
    def test_get_filter_fields_empty(self):
        """
        Test :py:meth:`.MultipleObjectMixin.get_filter_fields` with emty result
        """
        mixin = MultipleObjectMixin()
        self.assertEqual({}, mixin.get_filter_fields())

    def test_get_filter_fields(self):
        """
        Test :py:meth:`.MultipleObjectMixin.get_filter_fields`.
        """
        mixin = MultipleObjectMixin()
        mixin.kwargs = {
            'category': 'foo',
            'username': 'bar',
        }
        mixin.filter_fields = {
            'cat': 'category',
            'user': 'username',
        }
        self.assertEqual({
            'cat': 'foo',
            'user': 'bar',
        }, mixin.get_filter_fields())

    def test_get_queryset(self):
        """
        Test :py:meth:`.MultipleObjectMixin.get_queryset`.
        """
        mixin = MultipleObjectMixin()
        mixin.document_class = Mock()
        self.assertEqual(mixin.document_class.objects, mixin.get_queryset())

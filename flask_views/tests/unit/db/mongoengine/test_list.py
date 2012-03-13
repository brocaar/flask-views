import unittest2 as unittest

from mock import Mock, patch

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

    def test_page_number_kwargs(self):
        """
        Test :py:meth:`.MultipleObjectMixin.get_page_number`.

        This tests retrieving the page number from the URL route arguments.

        """
        mixin = MultipleObjectMixin()
        mixin.kwargs = {
            'page': 10,
        }
        self.assertEqual(10, mixin.get_page_number())

    @patch('flask_views.db.mongoengine.list.request')
    def test_page_number_request_args(self, request):
        """
        Test :py:meth:`.MultipleObjectMixin.get_page_number`.

        This tests retrieving the page number from the request arguments.

        """
        request.args = {
            'page': '10',
        }
        mixin = MultipleObjectMixin()
        mixin.kwargs = {}
        self.assertEqual(10, mixin.get_page_number())

    @patch('flask_views.db.mongoengine.list.request')
    def test_page_number_no_page(self, request):
        """
        Test :py:meth:`.MultipleObjectMixin.get_page_number` without given page
        """
        request.args = {}
        mixin = MultipleObjectMixin()
        mixin.kwargs = {}
        self.assertEqual(1, mixin.get_page_number())

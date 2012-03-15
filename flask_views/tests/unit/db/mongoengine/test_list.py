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

    def test_get_object_list_no_pagination(self):
        """
        Test :py:meth:`.MultipleObjectMixin.get_object_list` without pagination
        """
        query_set = Mock()

        mixin = MultipleObjectMixin()
        mixin.get_queryset = Mock(return_value=query_set)

        self.assertEqual(query_set.all.return_value, mixin.get_object_list())
        query_set.all.assert_called_once_with()

    def test_get_object_list(self):
        """
        Test :py:meth:`.MultipleObjectMixin.get_object_list` with pagination.
        """
        class DummyQuerySet(object):
            def __getitem__(self, item):
                return '{0}:{1}'.format(item.start, item.stop)

        mixin = MultipleObjectMixin()
        mixin.get_queryset = Mock(return_value=DummyQuerySet())
        mixin.items_per_page = 10

        for index, expected in enumerate(['0:10', '10:20', '20:30']):
            mixin.get_page_number = Mock(return_value=index + 1)
            self.assertEqual(expected, mixin.get_object_list())

    @patch('flask_views.db.mongoengine.list.abort')
    def test_get_object_list_404(self, abort):
        """
        Test :py:meth:`.MultipleObjectMixin.get_object_list` returning 404.
        """
        mixin = MultipleObjectMixin()
        mixin.items_per_page = 10
        mixin.get_page_number = Mock(return_value=2)
        mixin.get_queryset = Mock(side_effect=IndexError)
        self.assertEqual(None, mixin.get_object_list())
        abort.assert_called_once_with(404)

    def test_get_context_object_name_set(self):
        """
        Test :py:meth:`.MultipleObjectMixin.get_context_object_name`.

        This tests with ``context_object_name`` variable set.

        """
        mixin = MultipleObjectMixin()
        mixin.context_object_name = 'myobject_list'
        self.assertEqual('myobject_list', mixin.get_context_object_name())

    def test_get_ontext_object_name_from_object(self):
        """
        Test :py:meth:`.MultipleObjectMixin.get_context_object_name`.

        This tests generating the object name from the document class.

        """
        class MyObject(object):
            pass

        mixin = MultipleObjectMixin()
        mixin.document_class = MyObject
        self.assertEqual('myobject_list', mixin.get_context_object_name())

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

    def test_get_filtered_queryset(self):
        """
        Test :py:meth:`~.MultipleObjectMixin.get_filtered_queryset`.
        """
        queryset = Mock()

        mixin = MultipleObjectMixin()
        mixin.get_filter_fields = Mock(
            return_value={'foo': 'bar', 'bar': 'foo'})
        mixin.get_queryset = Mock(return_value=queryset)

        self.assertEqual(
            queryset.filter.return_value, mixin.get_filtered_queryset())
        queryset.filter.assert_called_once_with(foo='bar', bar='foo')

    def test_get_filtered_queryset_no_filters(self):
        """
        Test :py:meth:`~.MultipleObjectMixin.get_filtered_queryset`.

        This tests the result without filters.

        """
        mixin = MultipleObjectMixin()
        mixin.get_filter_fields = Mock(return_value={})
        mixin.get_queryset = Mock()

        self.assertEqual(
            mixin.get_queryset.return_value, mixin.get_filtered_queryset())

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

    def test_page_count_not_items_per_page(self):
        """
        Test :py:meth:`.MultipleObjectMixin.get_page_count` without pagination.
        """
        mixin = MultipleObjectMixin()
        self.assertEqual(None, mixin.get_page_count())

    def test_page_count_with_items_per_page(self):
        """
        Test :py:meth:`.MultipleObjectMixin.get_page_count` with pagination.
        """
        filtered_queryset = Mock()

        mixin = MultipleObjectMixin()
        mixin.items_per_page = 5
        mixin.get_filtered_queryset = Mock(return_value=filtered_queryset)

        for total_items, expected_page_count in (
                    (1, 1),
                    (5, 1),
                    (6, 2),
                    (10, 2),
                    (11, 3),
                ):
            filtered_queryset.count.return_value = total_items
            self.assertEqual(expected_page_count, mixin.get_page_count())

    def test_get_paginated_object_list_no_pagination(self):
        """
        Test :py:meth:`.MultipleObjectMixin.get_paginated_object_list`.

        This tests the return without pagination.

        """
        mixin = MultipleObjectMixin()
        mixin.get_filtered_queryset = Mock()

        self.assertEqual(
            mixin.get_filtered_queryset.return_value,
            mixin.get_paginated_object_list()
        )

    def test_get_paginated_object_list(self):
        """
        Test :py:meth:`.MultipleObjectMixin.get_paginated_object_list`.
        """
        class DummyQuerySet(object):
            def __getitem__(self, item):
                return '{0}:{1}'.format(item.start, item.stop)

        mixin = MultipleObjectMixin()
        mixin.get_filtered_queryset = Mock(return_value=DummyQuerySet())
        mixin.items_per_page = 10

        for index, expected in enumerate(['0:10', '10:20', '20:30']):
            mixin.get_page_number = Mock(return_value=index + 1)
            self.assertEqual(expected, mixin.get_paginated_object_list())

    @patch('flask_views.db.mongoengine.list.abort')
    def test_get_paginated_object_list_404(self, abort):
        """
        Test :py:meth:`.MultipleObjectMixin.get_paginated_object_list`.

        This tests a 404 return.

        """
        mixin = MultipleObjectMixin()
        mixin.items_per_page = 10
        mixin.get_page_number = Mock(return_value=2)
        mixin.get_filtered_queryset = Mock(side_effect=IndexError)
        self.assertEqual(None, mixin.get_paginated_object_list())
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

    def test_get_context_data_is_paginated(self):
        """
        Test :py:meth:`.MultipleObjectMixin.get_context_data` paginated.
        """
        mixin = MultipleObjectMixin()
        mixin.items_per_page = 1
        mixin.get_context_object_name = Mock(return_value='foo_bar')
        mixin.get_paginated_object_list = Mock()

        self.assertEqual({
            'foo': 'bar',
            'is_paginated': True,
            'items_per_page': 1,
            'foo_bar': mixin.get_paginated_object_list.return_value,
        }, mixin.get_context_data(foo='bar'))

    def test_get_context_data_unpaginated(self):
        """
        Test :py:meth:`.MultipleObjectMixin.get_context_data` unpaginated.
        """
        mixin = MultipleObjectMixin()
        mixin.get_context_object_name = Mock(return_value='foo_bar')
        mixin.get_paginated_object_list = Mock()

        self.assertEqual({
            'foo': 'bar',
            'is_paginated': False,
            'items_per_page': 0,
            'foo_bar': mixin.get_paginated_object_list.return_value,
        }, mixin.get_context_data(foo='bar'))

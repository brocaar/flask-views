from unittest import TestCase

from mock import Mock

from flask_views.db.mongoengine.detail import SingleObjectMixin


class SingleObjectMixinTestCase(TestCase):
    """
    Tests for :py:class:`.SingleObjectMixin`.
    """
    def test_get_context_object_name_from_attr(self):
        """
        Test :py:meth:`.SingleObjectMixin.get_context_object_name` from attr.
        """
        mixin = SingleObjectMixin()
        mixin.context_object_name = 'foo'
        self.assertEqual('foo', mixin.get_context_object_name())

    def test_get_context_object_name_from_obj(self):
        """
        Test :py:meth:`.SingleObjectMixin.get_context_object_name` from obj.
        """
        class Foo(object):
            pass

        class Bar(object):
            pass

        for class_obj, expected in [
                    (Foo, 'foo'),
                    (Bar, 'bar'),
                ]:
            mixin = SingleObjectMixin()
            mixin.model = class_obj
            self.assertEqual(expected, mixin.get_context_object_name())

    def test_get_queryset(self):
        """
        Test :py:meth:`.SingleObjectMixin.get_queryset`.
        """
        mixin = SingleObjectMixin()
        mixin.model = Mock()
        mixin.model.objects = 'objects-qs'
        self.assertEqual('objects-qs', mixin.get_queryset())

    def test_get_object(self):
        """
        Test :py:meth:`.SingleObjectMixin.get_object` on single field.
        """
        queryset = Mock()
        queryset.get.return_value = 'object'

        mixin = SingleObjectMixin()
        mixin.get_queryset = Mock(return_value=queryset)
        mixin.get_fields = {
            'db_id': 'url_id',
        }
        mixin.kwargs = {
            'url_id': '1234abc',
        }

        result = mixin.get_object()
        queryset.get.assert_called_once_with(db_id='1234abc')
        self.assertEqual('object', result)

    def test_get_object_multi_field(self):
        """
        Test py:meth:`.SingleObjectMixin.get_object` on multiple fields.
        """
        queryset = Mock()
        queryset.get.return_value = 'object'

        mixin = SingleObjectMixin()
        mixin.get_queryset = Mock(return_value=queryset)
        mixin.get_fields = {
            'db_id': 'url_id',
            'db_user': 'url_user',
        }
        mixin.kwargs = {
            'url_id': '1234abc',
            'url_user': 'foobar',
        }

        result = mixin.get_object()
        queryset.get.assert_called_once_with(db_id='1234abc', db_user='foobar')
        self.assertEqual('object', result)

    def test_get_object_not_found(self):
        """
        Test :py:meth:`.SingleObjectMixin.get_object` raising 404 exception.
        """
        mixin = SingleObjectMixin()
        mixin.model = Mock()
        mixin.model.DoesNotExist = Exception

        queryset = Mock()
        queryset.get.side_effect = mixin.model.DoesNotExist('Boom!')

        mixin.get_queryset = Mock(return_value=queryset)
        mixin.kwargs = {
            'id': '1234abc',
        }

        self.assertRaises(mixin.model.DoesNotExist, mixin.get_object)

import unittest2 as unittest

from mock import Mock

from flask_views.base import View, TemplateResponseMixin
from flask_views.db.mongoengine.detail import (
    SingleObjectMixin, BaseDetailView, DetailView
)


class SingleObjectMixinTestCase(unittest.TestCase):
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
            mixin.document_class = class_obj
            self.assertEqual(expected, mixin.get_context_object_name())

    def test_get_queryset(self):
        """
        Test :py:meth:`.SingleObjectMixin.get_queryset`.
        """
        mixin = SingleObjectMixin()
        mixin.document_class = Mock()
        mixin.document_class.objects = 'objects-qs'
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
        Test :py:meth:`.SingleObjectMixin.get_object` on multiple fields.
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
        mixin.document_class = Mock()
        mixin.document_class.DoesNotExist = Exception

        queryset = Mock()
        queryset.get.side_effect = mixin.document_class.DoesNotExist('Boom!')

        mixin.get_queryset = Mock(return_value=queryset)
        mixin.kwargs = {
            'id': '1234abc',
        }

        self.assertRaises(mixin.document_class.DoesNotExist, mixin.get_object)

    def test_get_context_data(self):
        """
        Test :py:meth:`.SingleObjectMixin.get_context_data`.
        """
        mixin = SingleObjectMixin()
        mixin.object = Mock()
        mixin.get_context_object_name = Mock(return_value='obj_name')
        self.assertEqual({
            'foo': 'bar',
            'obj_name': mixin.object,
        }, mixin.get_context_data(foo='bar'))


class BaseDetailViewTestCase(unittest.TestCase):
    """
    Tests for :py:class:`.BaseDetailView`.
    """
    def test_inherited_classes(self):
        """
        Test that it extends :class:`.SingleObjectMixin` and :class:`.View`.
        """
        self.assertEqual([SingleObjectMixin, View], BaseDetailView.mro()[1:3])

    def test_get(self):
        """
        Test :py:meth:`.BaseDetailView.get`.
        """
        view = BaseDetailView()
        view.get_object = Mock(return_value='object')
        view.get_context_data = Mock(return_value={'foo': 'bar'})
        view.render_to_response = Mock(return_value='response')

        self.assertEqual('response', view.get())
        self.assertEqual('object', view.object)
        view.render_to_response.assert_called_once_with({'foo': 'bar'})


class DetailViewTestCase(unittest.TestCase):
    """
    Tests for :py:class:`.DetailView`.
    """
    def test_inherited_classes(self):
        """
        Test that it inherits from the right classes.
        """
        self.assertEqual(
            [TemplateResponseMixin, BaseDetailView],
            DetailView.mro()[1:3],
        )

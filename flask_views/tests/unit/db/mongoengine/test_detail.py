from unittest import TestCase

from flask_views.db.mongoengine.detail import SingleObjectMixin


class SingleObjectMixinTestCase(TestCase):
    """
    Tests for :py:class:`.SingleObjectMixin`.
    """
    def test_get_context_object_name_from_attr(self):
        """
        Test :py:class:`.SingleObjectMixin.get_context_object_name` from attr.
        """
        mixin = SingleObjectMixin()
        mixin.context_object_name = 'foo'
        self.assertEqual('foo', mixin.get_context_object_name())

    def test_get_context_object_name_from_obj(self):
        """
        Test :py:class:`.SingleObjectMixin.get_context_object_name` from obj.
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

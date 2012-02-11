from unittest import TestCase

from mock import Mock, patch

from flask_views.base import View, TemplateResponseMixin
from flask_views.db.mongoengine.detail import SingleObjectMixin
from flask_views.db.mongoengine.edit import (
    ModelFormMixin, BaseCreateView, CreateView, BaseUpdateView
)
from flask_views.edit import FormMixin, ProcessFormMixin


class ModelFormMixinTestCase(TestCase):
    """
    Tests for :py:class:`.ModelFormMixin`.
    """
    def test_inherited_classes(self):
        """
        Test that this class inherits from the right classes.
        """
        for class_obj in [FormMixin, SingleObjectMixin]:
            self.assertIn(class_obj, ModelFormMixin.mro())

    @patch('flask_views.db.mongoengine.edit.super', create=True)
    def test_get_form_kwargs(self, super_mock):
        """
        Test :py:meth:`.ModelFormMixin.get_form_kwargs`.
        """
        super_class = Mock()
        super_class.get_form_kwargs.return_value = {'foo': 'bar'}
        super_mock.return_value = super_class

        mixin = ModelFormMixin()
        mixin.object = Mock()

        self.assertEqual({
            'foo': 'bar',
            'obj': mixin.object,
        }, mixin.get_form_kwargs())
        super_mock.assert_called_once_with(ModelFormMixin, mixin)

    @patch('flask_views.db.mongoengine.edit.super', create=True)
    def test_form_valid(self, super_mock):
        """
        Test :py:meth:`.ModelFormMixin.form_valid`.
        """
        super_class = Mock()
        super_class.form_valid.return_value = 'form-valid'
        super_mock.return_value = super_class

        form = Mock()
        mixin = ModelFormMixin()
        mixin.object = Mock()

        self.assertEqual('form-valid', mixin.form_valid(form))
        form.populate_obj.assert_called_once_with(mixin.object)
        mixin.object.save.assert_called_once_with()
        super_mock.assert_called_once_with(ModelFormMixin, mixin)
        super_class.form_valid.assert_called_once_with(form)


class BaseCreateViewTestCase(TestCase):
    """
    Tests for :py:class:`.BaseCreateView`.
    """
    def test_inherited_classes(self):
        """
        Test that this class inherits from the right classes.
        """
        for class_obj in [ModelFormMixin, ProcessFormMixin, View]:
            self.assertIn(class_obj, BaseCreateView.mro())

    @patch('flask_views.db.mongoengine.edit.super', create=True)
    def test_get(self, super_mock):
        """
        Test :py:meth:`.BaseCreateView.get`.
        """
        super_class = Mock()
        super_class.get.return_value = 'get-response'
        super_mock.return_value = super_class

        view = BaseCreateView()
        view.object = 'foo'

        self.assertEqual('get-response', view.get('something', foo='bar'))
        self.assertEqual(None, view.object)
        super_class.get.assert_called_once_with('something', foo='bar')

    @patch('flask_views.db.mongoengine.edit.super', create=True)
    def test_post(self, super_mock):
        """
        Test :py:meth:`.BaseCreateView.post`.
        """
        super_class = Mock()
        super_class.post.return_value = 'post-response'
        super_mock.return_value = super_class

        view = BaseCreateView()
        view.model = Mock(return_value='model-instance')

        self.assertEqual('post-response', view.post('something', foo='bar'))
        self.assertEqual('model-instance', view.object)
        super_class.post.assert_called_once_with('something', foo='bar')


class CreateViewTestCase(TestCase):
    """
    Tests for :py:class:`.CreateView`.
    """
    def test_inherited_classes(self):
        """
        Test that this class inherits from the right classes.
        """
        for class_obj in [TemplateResponseMixin, BaseCreateView]:
            self.assertIn(class_obj, CreateView.mro())


class BaseUpdateViewTestCase(TestCase):
    """
    Tests for :py:class:`.BaseUpdateView`.
    """
    @patch('flask_views.db.mongoengine.edit.super', create=True)
    def test_get(self, super_mock):
        """
        Test :py:meth:`.BaseUpdateView.get`.
        """
        super_class = Mock()
        super_class.get.return_value = 'get-response'
        super_mock.return_value = super_class

        view = BaseUpdateView()
        view.get_object = Mock(return_value='object')

        self.assertEqual('get-response', view.get('someting', foo='bar'))
        self.assertEqual('object', view.object)
        super_class.get.assert_called_once_with('someting', foo='bar')

    @patch('flask_views.db.mongoengine.edit.super', create=True)
    def test_post(self, super_mock):
        """
        Test :py:meth:`.BaseUpdateView.post`.
        """
        super_class = Mock()
        super_class.post.return_value = 'post-response'
        super_mock.return_value = super_class

        view = BaseUpdateView()
        view.get_object = Mock(return_value='object')

        self.assertEqual('post-response', view.post('something', foo='bar'))
        self.assertEqual('object', view.object)
        super_class.post.assert_called_once_with('something', foo='bar')

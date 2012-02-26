import unittest2 as unittest

from mock import Mock, patch

from flask_views.base import View, TemplateResponseMixin
from flask_views.db.mongoengine.detail import SingleObjectMixin
from flask_views.db.mongoengine.edit import (
    ModelFormMixin, BaseCreateView, CreateView, BaseUpdateView, UpdateView
)
from flask_views.edit import FormMixin, ProcessFormMixin


class ModelFormMixinTestCase(unittest.TestCase):
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
    def test_form_valid_with_object(self, super_mock):
        """
        Test :py:meth:`.ModelFormMixin.form_valid` with ``self.object`` set.
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

    @patch('flask_views.db.mongoengine.edit.super', create=True)
    def test_form_valid_without_object(self, super_mock):
        """
        Test :py:meth:`.ModelFormMixin.form_valid` without ``self.object`` set.
        """
        super_class = Mock()
        super_class.form_valid.return_value = 'form-valid'
        super_mock.return_value = super_class

        form = Mock()
        model_obj = Mock()
        mixin = ModelFormMixin()
        mixin.object = None
        mixin.document_class = Mock(return_value=model_obj)

        self.assertEqual('form-valid', mixin.form_valid(form))
        form.populate_obj.assert_called_once_with(model_obj)
        mixin.object.save.assert_called_once_with()
        super_mock.assert_called_once_with(ModelFormMixin, mixin)
        super_class.form_valid.assert_called_once_with(form)

    @patch('flask_views.db.mongoengine.edit.super', create=True)
    def test_get_context_data(self, super_mock):
        """
        Test :py:meth:`.ModelFormMixin.get_context_data`.
        """
        super_class = Mock()
        super_class.get_context_data.return_value = {'foo': 'bar'}
        super_mock.return_value = super_class

        mixin = ModelFormMixin()
        mixin.object = Mock()

        self.assertEqual({
            'foo': 'bar',
            'object': mixin.object,
        }, mixin.get_context_data(foo='bar'))
        super_class.get_context_data.assert_called_once_with(foo='bar')


class BaseCreateViewTestCase(unittest.TestCase):
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
        view.object = 'foo'

        self.assertEqual('post-response', view.post('something', foo='bar'))
        self.assertEqual(None, view.object)
        super_class.post.assert_called_once_with('something', foo='bar')


class CreateViewTestCase(unittest.TestCase):
    """
    Tests for :py:class:`.CreateView`.
    """
    def test_inherited_classes(self):
        """
        Test that this class inherits from the right classes.
        """
        for class_obj in [TemplateResponseMixin, BaseCreateView]:
            self.assertIn(class_obj, CreateView.mro())


class BaseUpdateViewTestCase(unittest.TestCase):
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


class UpdateViewTestCase(unittest.TestCase):
    """
    Tests for :py:class:`.UpdateView`.
    """
    def test_inherited_classes(self):
        for class_obj in [TemplateResponseMixin, BaseUpdateView]:
            self.assertIn(class_obj, UpdateView.mro())

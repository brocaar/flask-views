import unittest

from mock import Mock, patch

from flask_views.edit import FormMixin


class FormMixinTestCase(unittest.TestCase):
    """
    Tests for :py:class:`.FormMixin`.
    """
    def test_initial(self):
        """
        Test :py:meth:`.FormMixin.get_initial`.
        """
        mixin = FormMixin()
        mixin.initial = {'foo': 'bar'}

        self.assertEqual({'foo': 'bar'}, mixin.get_initial())

    def test_get_context_data(self):
        """
        Test :py:meth:`.FormMixin.get_context_data`.
        """
        mixin = FormMixin()
        self.assertEqual({'foo': 'bar'}, mixin.get_context_data(foo='bar'))

    @patch('flask_views.edit.request')
    def test_get_form_kwargs(self, request):
        """
        Test :py:meth:`.FormMixin.get_form_kwargs`.
        """
        request.form = {'foo': 'bar'}

        mixin = FormMixin()
        mixin.get_initial = Mock(return_value={'name': 'John'})

        self.assertEqual({
            'formdata': {'foo': 'bar'},
            'name': 'John',
        }, mixin.get_form_kwargs())
        mixin.get_initial.assert_called_once_with()

    def test_get_form(self):
        """
        Test :py:meth:`.FormMixin.get_form`.
        """
        mixin = FormMixin()
        mixin.form = Mock(return_value='form-instance')
        mixin.get_form_kwargs = Mock(return_value={'foo': 'bar'})

        self.assertEqual('form-instance', mixin.get_form())
        mixin.get_form_kwargs.assert_called_once_with()
        mixin.form.assert_called_once_with(foo='bar')

import unittest2 as unittest

from mock import Mock, patch

from flask_views.edit import FormMixin, ProcessFormMixin


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

    def test_get_success_url(self):
        """
        Test :py:meth:`.FormMixin.get_success_url`.
        """
        mixin = FormMixin()
        mixin.success_url = 'foo/bar'

        self.assertEqual('foo/bar', mixin.get_success_url())

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
        mixin.form_class = Mock(return_value='form-instance')
        mixin.get_form_kwargs = Mock(return_value={'foo': 'bar'})

        self.assertEqual('form-instance', mixin.get_form())
        mixin.get_form_kwargs.assert_called_once_with()
        mixin.form_class.assert_called_once_with(foo='bar')

    @patch('flask_views.edit.redirect')
    def test_form_valid(self, redirect):
        """
        Test :py:meth:`.FormMixin.form_valid`.
        """
        redirect.return_value = 'redirect'

        mixin = FormMixin()
        mixin.get_success_url = Mock(return_value='foo/bar')

        self.assertEqual('redirect', mixin.form_valid(Mock()))
        redirect.assert_called_once_with('foo/bar')

    def test_form_invalid(self):
        """
        Test :py:meth:`.FormMixin.form_invalid`.
        """
        mixin = FormMixin()
        mixin.get_context_data = Mock(return_value={'foo': 'bar'})
        mixin.render_to_response = Mock(return_value='response')

        form_mock = Mock()
        self.assertEqual('response', mixin.form_invalid(form=form_mock))
        mixin.get_context_data.assert_called_once_with(form=form_mock)
        mixin.render_to_response.assert_called_once_with({'foo': 'bar'})


class ProcessFormMixinTestCase(unittest.TestCase):
    """
    Tests for :py:class:`.ProcessFormMixin`.
    """
    def test_get(self):
        """
        Test :py:meth:`.ProcessFormMixin.get`.
        """
        mixin = ProcessFormMixin()
        mixin.get_form = Mock(return_value='form-instance')
        mixin.get_context_data = Mock(return_value={'context': 'data'})
        mixin.render_to_response = Mock(return_value='response')

        self.assertEqual('response', mixin.get())
        mixin.get_context_data.assert_called_once_with(form='form-instance')
        mixin.render_to_response.assert_called_once_with({'context': 'data'})

    def test_post_form_valid(self):
        """
        Test :py:meth:`.ProcessFormMixin.post` in case of a valid form.
        """
        form_instance = Mock()
        form_instance.validate.return_value = True

        mixin = ProcessFormMixin()
        mixin.get_form = Mock(return_value=form_instance)
        mixin.form_valid = Mock(return_value='valid-form')
        mixin.form_invalid = Mock(return_value='invalid-form')

        self.assertEqual('valid-form', mixin.post())
        form_instance.validate.assert_called_once_with()
        mixin.form_valid.assert_called_once_with(form_instance)
        self.assertEqual(0, mixin.form_invalid.call_count)

    def test_post_form_invalid(self):
        """
        Test :py:meth:`.ProcessFormMixin.post` in case of an invalid form.
        """
        form_instance = Mock()
        form_instance.validate.return_value = False

        mixin = ProcessFormMixin()
        mixin.get_form = Mock(return_value=form_instance)
        mixin.form_valid = Mock(return_value='valid-form')
        mixin.form_invalid = Mock(return_value='invalid-form')

        self.assertEqual('invalid-form', mixin.post())
        form_instance.validate.assert_called_once_with()
        mixin.form_invalid.assert_called_once_with(form_instance)
        self.assertEqual(0, mixin.form_valid.call_count)

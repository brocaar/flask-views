import unittest2 as unittest

from mock import patch, Mock

from flask_views.base import TemplateResponseMixin, TemplateView, View


class ViewTestCase(unittest.TestCase):
    """
    Tests for :py:class:`.View`.
    """
    @patch('flask_views.base.super', create=True)
    def test_dispatch_request(self, super_mock):
        """
        Test :py:meth:`.View.dispatch_request`.
        """
        super_class = Mock()
        super_class.dispatch_request.return_value = 'dispatch_request'
        super_mock.return_value = super_class

        view = View()

        self.assertEqual('dispatch_request', view.dispatch_request(
            'foo', 'bar', foo='bar'))

        self.assertEqual(('foo', 'bar'), view.args)
        self.assertEqual({'foo': 'bar'}, view.kwargs)
        super_mock.assert_called_once_with(View, view)
        super_class.dispatch_request.assert_called_once_with(
            'foo', 'bar', foo='bar')


class TemplateResponseMixinTestCase(unittest.TestCase):
    """
    Tests for :py:class:`.TemplateResponseMixin`.
    """
    @patch('flask_views.base.render_template')
    def test_render_to_response(self, render_template):
        """
        Test :py:meth:`.TemplateResponseMixin.render_to_response`.
        """
        render_template.return_value = 'rendered-template'

        mixin = TemplateResponseMixin()
        mixin.template_name = 'my/template.html'

        self.assertEqual(
            'rendered-template', mixin.render_to_response({'foo': 'bar'}))
        render_template.assert_called_once_with('my/template.html', foo='bar')


class TemplateViewTestCase(unittest.TestCase):
    """
    Tests for :py:class:`.TemplateView`.
    """
    def test_get_context_data(self):
        """
        Test :py:meth:`.TemplateView.get_context_data`.
        """
        view = TemplateView()
        self.assertEqual({
            'params': {
                'foo': 'bar',
            }
        }, view.get_context_data(foo='bar'))

    def test_get(self):
        """
        Test :py:meth:`.TemplateView.get`.
        """
        view = TemplateView()
        view.get_context_data = Mock(return_value={'foo': 'bar'})
        view.render_to_response = Mock(return_value='response')

        self.assertEqual('response', view.get(bar='foo'))
        view.get_context_data.assert_called_once_with(bar='foo')
        view.render_to_response.assert_called_once_with({'foo': 'bar'})

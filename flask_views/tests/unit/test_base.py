import unittest

from mock import patch

from flask_views.base import TemplateResponseMixin


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
            'rendered-template', mixin.render_to_response(foo='bar'))
        render_template.assert_called_once_with('my/template.html', foo='bar')

from unittest import TestCase

from mock import patch

from flask_views.json import JSONResponseMixin


class JSONResponseMixinTestCase(TestCase):
    """
    Tests for :py:class:`.JSONResponseMixin`.
    """
    @patch('flask_views.json.json')
    @patch('flask_views.json.current_app')
    def test_render_to_response(self, current_app, json):
        """
        Test :py:meth:`.JSONResponseMixin.render_to_response`.
        """
        current_app.response_class.return_value = 'response-class'
        json.dumps.return_value = 'json-dump'

        mixin = JSONResponseMixin()

        self.assertEqual(
            'response-class',
            mixin.render_to_response({'foo': 'bar'})
        )
        json.dumps.assert_called_once_with({'foo': 'bar'})
        current_app.response_class.assert_called_once_with(
            'json-dump', mimetype='application/json')

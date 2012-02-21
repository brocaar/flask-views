from __future__ import absolute_import
import json

from flask import current_app

from flask_views.base import View


class JSONResponseMixin(object):
    """
    Mixin class for rendering JSON responses.
    """
    encoder_class = None
    """
    Set this to your custom implementation of :py:class:`!json.JSONEncoder`
    if needed. Optional.
    """

    def render_to_response(self, context_data={}):
        """
        Render JSON response for the given context data.

        :param context_data:
            A ``dict`` containing the context data. Optional.

        :return:
            Output of :py:meth:`!flask.current_app.response_class` containing
            the JSON dump with ``'application/json'`` mimetype.

        """
        return current_app.response_class(
            json.dumps(context_data, cls=self.encoder_class),
            mimetype='application/json'
        )


class JSONView(JSONResponseMixin, View):
    """
    View class for rendering JSON responses.

    This class inherits from:

    * :py:class:`~flask_views.json.JSONResponseMixin`
    * :py:class:`.View`

    Example usage::

        class ExampleJSONView(JSONView):
            pass

    Requesting ``'/users/john/'`` with the URL route ``'/users/<user>/'`` will
    then result in the following JSON data::

        {
            "params": {
                "user": "john"
            }
        }

    Probably you want to override the :py:meth:`~.JSONView.get_context_data`
    method, to provide your own set of data that will be JSON encoded.

    """
    def get_context_data(self, **kwargs):
        """
        Get context data for rendering the JSON response.

        :return:
            A ``dict`` containing the following keys:

            ``params``
                A ``dict`` containing the ``kwargs``.

        """
        return {
            'params': kwargs,
        }

    def get(self, *args, **kwargs):
        """
        Render the JSON response on GET request.

        The keyword-arguments passed by the URL dispatcher are added
        to the context data.

        :return:
            Output of :py:meth:`.JSONResponseMixin.render_to_response`.

        """
        return self.render_to_response(self.get_context_data(**kwargs))

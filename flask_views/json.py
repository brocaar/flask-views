import json

from flask import current_app


class JSONResponseMixin(object):
    """
    Mixin class for rendering JSON responses.
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
            json.dumps(context_data),
            mimetype='application/json'
        )

from flask import render_template
from flask.views import MethodView


class View(MethodView):
    """
    View which will dispatch requests based on method.

    This class inherits from:

    * :py:class:`!flask.views.MethodView`

    """
    def dispatch_request(self, *args, **kwargs):
        """
        Dispatch the request based on HTTP method.

        This as well sets the arguments and keyword-arguments passed by the
        URL route dispatcher to ``self.args`` and ``self.kwargs``.

        """
        self.args = args
        self.kwargs = kwargs
        return super(View, self).dispatch_request(*args, **kwargs)


class TemplateResponseMixin(object):
    """
    Mixin class for rendering templates.
    """

    template_name = None
    """
    Name of the template to be rendered.
    """

    def render_to_response(self, **kwargs):
        """
        Render template with the given keyword arguments.

        :return:
            The rendered template as a string.

        """
        return render_template(self.template_name, **kwargs)


class TemplateView(TemplateResponseMixin, View):
    """
    View class for rendering templates.

    This class inherits from:

    * :py:class:`.TemplateResponseMixin`
    * :py:class:`.View`

    """
    def get_context_data(self, **kwargs):
        """
        Get context data for rendering template.

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
        Render the template on request.
        """
        return self.render_to_response(**self.get_context_data(**kwargs))

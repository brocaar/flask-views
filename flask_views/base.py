from flask import render_template
from flask.views import View


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
    """
    methods = ['GET']

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

    def dispatch_request(self, **kwargs):
        """
        Render the template on request.
        """
        return self.render_to_response(**self.get_context_data(**kwargs))

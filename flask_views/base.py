from flask import render_template


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

from flask import render_template
from flask.views import MethodView


class View(MethodView):
    """
    View which will dispatch requests based on request method.

    This class inherits from:

    * :py:class:`!flask.views.MethodView`

    Example usage::

        class MethodView(View):

            def get(self, *args, **kwargs):
                return 'Hello {0}'.format(self.kwargs.get('user'))

    When you have a URL route ``'/<user>/'`` and you request, ``/john/``, it
    will return ``'Hello john'``.

    """
    def dispatch_request(self, *args, **kwargs):
        """
        Dispatch the request based on HTTP method.

        This sets the arguments and keyword-arguments passed by the
        URL route dispatcher to ``self.args`` and ``self.kwargs``, then it will
        dispatch the request to the right method.

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
    Set this variable to the template you want to render.
    """

    def render_to_response(self, context_data={}):
        """
        Render template with the given context data.

        :param context_data:
            A ``dict`` containing the context data. Optional.

        :return:
            The rendered template as a string.

        """
        return render_template(self.template_name, **context_data)


class TemplateView(TemplateResponseMixin, View):
    """
    View class for rendering templates.

    This class inherits from:

    * :py:class:`.TemplateResponseMixin`
    * :py:class:`.View`

    Example usage::

        class IndexTemplateView(TemplateView):
            template_name = 'index.html'

    """
    def get_context_data(self, **kwargs):
        """
        Get context data for rendering the template.

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

        The keyword-arguments passed by the URL dispatcher are added
        to the context data.

        :return:
            Output of :py:meth:`.TemplateResponseMixin.render_to_response`.

        """
        return self.render_to_response(self.get_context_data(**kwargs))

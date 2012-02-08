from flask import request

from flask_views.base import TemplateResponseMixin, View


class FormMixin(object):
    """
    Mixin for handling forms.
    """
    form_class = None
    """
    The form class.
    """

    initial = {}
    """
    Initial data when creating form instance.
    """

    def get_initial(self):
        """
        Return initial form data.

        :return:
            :py:data:`flask_views.edit.FormMixin.initial`.

        """
        return self.initial

    def get_context_data(self, **kwargs):
        """
        Return a ``dict`` containing the context data.

        :return:
            A ``dict`` containing the given keyword arguments.

        """
        return kwargs

    def get_form_kwargs(self):
        """
        Return parameters for creating the form instance.

        :return:
            A ``dict`` containing the arguments for creating the form instance.

        """
        kwargs = {'formdata': request.form}
        kwargs.update(self.get_initial())
        return kwargs

    def get_form(self):
        """
        Return an instance of the form class.

        :return:
            Instance :py:class:`flask_views.edit.FormMixin.form_class`.

        """
        return self.form(**self.get_form_kwargs())

    def form_valid(self, form):
        """
        Handle valid form submission.

        Override this function with your own implementation.

        :param form:
            Instance of the form.

        :raise:
            :py:exc:`!NotImplementedError`.

        """
        raise NotImplementedError()

    def form_invalid(self, form):
        """
        Handle invalid form submission.

        This will render the response with the current ``form`` in the context
        so that the errors can be displayed to the user.

        :param form:
            Instance of the form class.

        :return:
            Response containing the ``form`` in the context.

        """
        return self.render_to_response(**self.get_context_data(form=form))


class ProcessFormMixin(object):
    """
    Mixin for processing form data on GET and POST requests.
    """
    def get(self, *args, **kwargs):
        """
        Handler for ``GET`` requests.
        """
        form = self.get_form()
        return self.render_to_response(**self.get_context_data(form=form))

    def post(self, *args, **kwargs):
        """
        Handler for ``POST`` requests.
        """
        form = self.get_form()
        if form.validate():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class BaseFormView(FormMixin, ProcessFormMixin, View):
    """
    Base view for displaying a form.

    This class inherits from:

    * :py:class:`.FormMixin`
    * :py:class:`.ProcessFormMixin`
    * :py:class:`.View`

    """


class FormView(TemplateResponseMixin, BaseFormView):
    """
    View for displaying a form and rendering a template.

    This class inherits from:

    * :py:class:`.TemplateResponseMixin`
    * :py:class:`.BaseFormView`

    """

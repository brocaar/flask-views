from flask import request, redirect

from flask_views.base import TemplateResponseMixin, View


class FormMixin(object):
    """
    Mixin for handling forms.
    """
    form_class = None
    """
    Set this to the form class (WTForms) you want to use.

    .. seealso:: http://wtforms.simplecodes.com/

    """

    initial = {}
    """
    Set this to the initial data for form fields. Example::

        initial = {
            'title': 'Initial title value',
            'body': 'Initial body value.',
        }

    """

    success_url = None
    """
    Set this to the URL the user should be redirected to after a successful
    form submittion.
    """

    def get_initial(self):
        """
        Return initial form data.

        :return:
            :py:data:`flask_views.edit.FormMixin.initial`.

        """
        return self.initial

    def get_success_url(self):
        """
        Return success URL.

        :return:
            :py:data:`flask_views.edit.FormMixin.success_url`.

        """
        return self.success_url

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
        return self.form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        """
        Handle valid form submission.

        This redirects the user to the URL returned by
        :py:meth:`flask_views.edit.FormMixin.get_success_url`. You want to
        override this method for processing the submitted form data.

        :param form:
            Instance of the form.

        :return:
            Redirect to URL returned by
            :py:meth:`flask_views.edit.FormMixin.get_success_url`.

        """
        return redirect(self.get_success_url())

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
    methods = ['GET', 'POST']

    def get(self, *args, **kwargs):
        """
        Handler for ``GET`` requests.

        This will call ``render_to_response`` with an instance of the form
        as ``form`` in the context data.

        :return:
            Output of ``render_to_response`` method implementation.

        """
        form = self.get_form()
        return self.render_to_response(**self.get_context_data(form=form))

    def post(self, *args, **kwargs):
        """
        Handler for ``POST`` requests.

        On a valid form submission, this will dispatch the request to
        the ``form_valid`` method, else it is dispatched to ``form_invalid``.

        :return:
            Output of ``form_valid`` or ``form_invalid``.

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

    This class implements all logic for processing forms, but does not include
    rendering responses. See :py:class:`.FormView` for an usage example.

    """


class FormView(TemplateResponseMixin, BaseFormView):
    """
    View for displaying a form, including rendering of template.

    This class inherits from:

    * :py:class:`.TemplateResponseMixin`
    * :py:class:`.BaseFormView`

    This class implements all logic for displaying and processing form
    submissions, including rendering of templates.

    Usage example::

        class ContactFormView(FormView):
            form_class = ContactForm
            template_name = 'contact_form.html'

            def form_valid(self, form):
                # Do something with the submitted form data
                return super(ContactFormView, self).form_valid(form)

            def get_success_url(self):
                return url_for('contact.form')

    An instance of the form class will be available in the template context
    under the ``form`` variable.

    """

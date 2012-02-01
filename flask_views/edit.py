from flask import request


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

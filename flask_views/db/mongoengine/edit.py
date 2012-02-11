from flask_views.base import View
from flask_views.db.mongoengine.detail import SingleObjectMixin
from flask_views.edit import FormMixin, ProcessFormMixin


class ModelFormMixin(FormMixin, SingleObjectMixin):
    """
    Mixin for handling model-form processing.

    This class inherits from:

    * :py:class:`.FormMixin`
    * :py:class:`.SingleObjectMixin`

    """
    def get_form_kwargs(self):
        """
        Return parameters for creating the form instance.

        :return:
            A ``dict`` containing the arguments for creating the form instance.

        """
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        kwargs['obj'] = self.object
        return kwargs

    def form_valid(self, form):
        """
        Handle a valid form submission.
        """
        self.object = self.model()
        form.populate_obj(self.object)
        self.object.save()
        return super(ModelFormMixin, self).form_valid(form)


class BaseCreateView(ModelFormMixin, ProcessFormMixin, View):
    """
    Base view for create forms.

    This class inherits from:

    * :py:class:`.ModelFormMixin`
    * :py:class:`.ProcessFormMixin`
    * :py:class:`.View`

    """
    def get(self, *args, **kwargs):
        """
        Handler for GET requests.
        """
        self.object = None
        return super(BaseCreateView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Handler for POST requests.
        """
        self.object = None
        return super(BaseCreateView, self).post(*args, **kwargs)

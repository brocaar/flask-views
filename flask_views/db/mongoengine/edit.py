from flask_views.base import TemplateResponseMixin, View
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

        This adds a model instance (or ``None``) to the form parameters
        returned by :py:meth:`.FormMixin.get_form_kwargs`.

        :return:
            A ``dict`` containing the arguments for creating the form instance.

        """
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        kwargs['obj'] = self.object
        return kwargs

    def form_valid(self, form):
        """
        Handle a valid form submission.

        When editing an object, the object will be updated and saved, else
        a new object will be created and saved.

        :return:
            Output returned by :py:meth:`.FormMixin.form_valid`.

        """
        if not self.object:
            self.object = self.document_class()
        form.populate_obj(self.object)
        self.object.save()
        return super(ModelFormMixin, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Return context data for rendering template.

        This adds ``self.object`` as ``object`` to the context data returned
        by :py:meth:`.FormMixin.get_context_data`.

        :return:
            A ``dict`` containing the context data.

        """
        context = super(ModelFormMixin, self).get_context_data(**kwargs)
        context.update({
            'object': self.object,
        })
        return context


class BaseCreateView(ModelFormMixin, ProcessFormMixin, View):
    """
    Base view for creating objects.

    This class inherits from:

    * :py:class:`.ModelFormMixin`
    * :py:class:`.ProcessFormMixin`
    * :py:class:`.View`

    This implements all logic for creating objects, but does not implement
    the rendering of responses. See :py:class:`.CreateView` for an usage
    example.

    """
    def get(self, *args, **kwargs):
        """
        Handler for GET requests.

        This will set ``self.object`` to ``None``.

        :return:
            Output returned by :py:meth:`.ProcessFormMixin.get`.

        """
        self.object = None
        return super(BaseCreateView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Handler for POST requests.

        This will set ``self.object`` to ``None``.

        :return:
            Output returned by :py:meth:`.ProcessFormMixin.post`.

        """
        self.object = None
        return super(BaseCreateView, self).post(*args, **kwargs)


class CreateView(TemplateResponseMixin, BaseCreateView):
    """
    View for creating objects.

    This class inherits from:

    * :py:class:`.TemplateResponseMixin`
    * :py:class:`.BaseCreateView`

    This implements all logic for creating objects, including the rendering
    of a template. Usage example::

        class PostCreateView(CreateView):
            form_class = PostForm
            document_class = Post
            template_name = 'post_form.html'

            def get_success_url(self):
                return url_for('posts.index')

    """


class BaseUpdateView(ModelFormMixin, ProcessFormMixin, View):
    """
    Base view for updating objects.

    This class inherits from:

    * :py:class:`.ModelFormMixin`
    * :py:class:`.ProcessFormMixin`

    This implements all logic for retrieving the object for updating and
    processing the form. This does not implement rendering the responses.
    See :py:class:`.UpdateView` for an usage example.

    """
    def get(self, *args, **kwargs):
        """
        Handler for GET requests.
        """
        self.object = self.get_object()
        return super(BaseUpdateView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Handler for POST requests.
        """
        self.object = self.get_object()
        return super(BaseUpdateView, self).post(*args, **kwargs)


class UpdateView(TemplateResponseMixin, BaseUpdateView):
    """
    View for updating objects.

    This class inherits from:

    * :py:class:`.TemplateResponseMixin`
    * :py:class:`.BaseUpdateView`

    This implements all logic for retrieving the object for updating and
    processing the form. As well this implements the rendering of a template.
    Usage example::

        class PostUpdateView(UpdateView):
            form_class = PostForm
            document_class = Post
            template_name = 'post_form.html'

            def get_success_url(self):
                url_for('posts.index')

    .. seealso:: :py:attr:`.SingleObjectMixin.get_fields` for more information
        about how the object is retrieved from the database.

    """

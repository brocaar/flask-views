from flask import abort

from flask_views.base import View, TemplateResponseMixin


class SingleObjectMixin(object):
    """
    Mixin for retrieving a single object from the database.
    """
    document_class = None
    """
    Document class from which the object should be retrieved.

    .. seealso:: http://mongoengine.org/

    """

    get_fields = {
        'id': 'id',
    }
    """
    A ``dict`` containing the fieldname mapped against the URL variable name.
    For example when you have the URL route ``'/<category>/<author>/'``, and
    the following setting::

        get_fields = {
            'cat': 'category',
            'user': 'author',
        }

    When requesting ``/news/john/``, it would perform the following query:
    ``get(cat='news', user='john')``.

    """

    context_object_name = None
    """
    The variable name to give this object in the template context. If ``None``,
    it will get the name of the model class (Eg: a class ``Page`` would be
    available as ``page``).

    """
    def get_context_object_name(self):
        """
        Return the context object name.

        If :py:attr:`.SingleObjectMixin.context_object_name` is set, that value
        will be returned, else it will use the lowercased name of the model
        set in :py:attr:`.SingleObjectMixin.document_class`.

        :return:
            A ``str`` representing the object name.

        """
        if self.context_object_name:
            return self.context_object_name

        return self.document_class.__name__.lower()

    def get_queryset(self):
        """
        Return ``QuerySet`` class used to retrieve objects.

        :return:
            An instance of :py:class:`!mongoengine.queryset.QuerySet`.

        """
        return self.document_class.objects

    def get_object(self):
        """
        Retrieve the object from the database.

        :return:
            An instance of the model class containing the retrieved object.

        :raise:
            :py:exc:`!werkzeug.exceptions.NotFound` when the document does not
            exist.

        """
        lookup_args = {}

        for field_name, mapping_name in self.get_fields.items():
            lookup_args[field_name] = self.kwargs.get(mapping_name, None)

        try:
            return self.get_queryset().get(**lookup_args)
        except self.document_class.DoesNotExist:
            abort(404)

    def get_context_data(self, **kwargs):
        """
        Return context data containing the retrieved object.

        :return:
            A ``dict`` containing the retrieved object.

        """
        kwargs[self.get_context_object_name()] = self.object
        return kwargs


class BaseDetailView(SingleObjectMixin, View):
    """
    Base detail view.

    This class inherits from:

    * :py:class:`.SingleObjectMixin`
    * :py:class:`.View`

    This class implements all logic for retrieving a single object from the
    database, but does not implement rendering responses. See
    :py:class:`.DetailView` for an usage example.

    """
    def get(self, *args, **kwargs):
        """
        Handler for GET requests.

        This retrieves the object from the database and calls the
        ``render_to_response`` with the retrieved object in the context
        data.

        :return:
            Ouput of ``render_to_response`` method implementation.

        """
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())


class DetailView(TemplateResponseMixin, BaseDetailView):
    """
    Detail view for rendering an object.

    This class inherits from:

    * :py:class:`.TemplateResponseMixin`
    * :py:class:`.BaseDetailView`

    This class implements all logic for retrieving a single object from the
    database, including rendering a template.

    Usage example::

        class ArticleView(DetailView):
            get_fields = {
                'category': 'category',
                'slug': 'slug',
            }
            document_class = Article
            template_name = 'article_detail.html'

    """

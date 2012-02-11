from flask import abort


class SingleObjectMixin(object):
    """
    Mixin for retrieving a single object from the database.
    """
    model = None
    """
    Document model class from which the object should be retrieved.
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
    it will get the name of the model class (Eg: a class ``Page`` would get
    stored as ``page``).

    """
    def get_context_object_name(self):
        """
        Return the context object name.

        If :py:attr:`.SingleObjectMixin.context_object_name` is set, that value
        will be returned, else it will use the lowercased name of the model
        set in :py:attr:`.SingleObjectMixin.model`.

        :return:
            A ``str`` representing the object name.

        """
        if self.context_object_name:
            return self.context_object_name

        return self.model.__name__.lower()

    def get_queryset(self):
        """
        Return ``QuerySet`` class used to retrieve objects.

        :return:
            An instance of :py:class:`!mongoengine.queryset.QuerySet`.

        """
        return self.model.objects

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
        except self.model.DoesNotExist:
            abort(404)

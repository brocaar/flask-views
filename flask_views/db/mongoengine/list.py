


class MultipleObjectMixin(object):
    """
    Mixin for retrieving multiple objects from the database.
    """
    document_class = None
    """
    Document class from which the objects should be retrieved.

    .. seealso:: http://mongoengine.org/

    """
    filter_fields = {}
    """
    A ``dict`` containing the fieldname mapped against the URL variable name.
    For example when you have the URL route ``'/<category>/<author>/'``, and
    the following setting::

        get_fields = {
            'cat': 'category',
            'user': 'author',
        }

    When requesting ``/news/john/``, it would perform the following query:
    ``filter(cat='news', user='john')``.

    When the result should not be filtered, set this to ``{}`` (default).

    """
    def get_filter_fields(self):
        """
        Return a ``dict`` with the fields to filter on.

        For generating this dictionary, the configuration in
        :py:attr:`~.MultipleObjectMixin.filter_fields` is used.

        :return:
            A ``dict`` with as the key the fieldname and as value the value to
            filter on. When the result should not be filtered, it returns an
            empty dict.

        """
        filter_fields = {}

        for field_name, mapping_name in self.filter_fields.items():
            filter_fields[field_name] = self.kwargs.get(mapping_name, None)

        return filter_fields

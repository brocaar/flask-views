from flask import abort, request


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

    page_number_argument = 'page'
    """
    A ``str`` representing the argument which should be used to retrieve the
    current page.
    """

    items_per_page = 0
    """
    An ``int`` representing the number of items that should be displayed per
    page. Set this to ``0`` when no pagination should be applied.
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

    def get_queryset(self):
        """
        Return ``QuerySet`` class used to retrieve objects.

        :return:
            An instance of :py:class:`!mongoengine.qeryset.QuerySet`.

        """
        return self.document_class.objects

    def get_page_number(self):
        """
        Return page number.

        This will first try to get the current page number from the URL route
        arguments. Failing that, it will try to retrieve the current page from
        the URL parameters. Failing that, ``1`` is returned.

        .. note:: This uses the name specified
            in :py:attr:`~.MultipleObjectMixin.page_number_argument`.

        :return:
            An ``int`` representing the current page number.

        """
        try:
            return self.kwargs[self.page_number_argument]
        except KeyError:
            try:
                return int(request.args[self.page_number_argument])
            except (KeyError, ValueError):
                return 1

    def get_object_list(self):
        """
        Return (optionally paginated) list of objects.

        When :py:attr:`~.MultipleObjectMixin.items_per_page` is not ``0``, this
        list will be paginated.

        :return:
            A ``list`` of objects.

        """
        if not self.items_per_page:
            return self.get_queryset().all()

        start_index = (self.get_page_number() - 1) * self.items_per_page
        end_index = self.get_page_number() * self.items_per_page

        try:
            return self.get_queryset()[start_index:end_index]
        except IndexError:
            abort(404)

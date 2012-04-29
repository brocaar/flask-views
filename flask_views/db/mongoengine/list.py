from math import ceil

from flask import abort, request

from flask_views.base import View, TemplateResponseMixin


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

    context_object_name = None
    """
    The variable name for the list of objects in the template context. If
    ``None``, it will get the name of the model class (Eg: a class ``Page``
    would be available as ``page_list``).
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

    def get_filtered_queryset(self):
        """
        Return filtered instance of ``QuerySet``.

        .. note:: This uses the filter fields defined
            in :py:attr:`~.MultipleObjectMixin.filter_fields`.

        :return:
            An instance of :py:class:`!mongoengine.qeryset.QuerySet`.

        """
        filter_fields_dict = self.get_filter_fields()

        if not filter_fields_dict:
            return self.get_queryset()

        return self.get_queryset().filter(**filter_fields_dict)

    def get_page_number(self):
        """
        Return page number.

        This will first try to get the current page number from the URL route
        arguments. Failing that, it will try to retrieve the current page from
        the URL parameters. Failing that, ``1`` is returned.

        .. note:: This uses the name specified
            in :py:attr:`~.MultipleObjectMixin.page_number_argument`.

        .. warning:: Make sure you cast the URL route argument for the page
            number to an ``int``. Example: ``/<category>/<int:page>/``.

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

    def get_page_count(self):
        """
        Return the total number of pages.

        :return:
            An ``int`` representing the total number of available pages or
            ``None`` when :py:attr:`~.MultipleObjectMixin.items_per_page` is
            set to ``0``.

        """
        if not self.items_per_page:
            return None

        count = self.get_filtered_queryset().count()
        return int(ceil(float(count) / float(self.items_per_page)))

    def get_paginated_object_list(self):
        """
        Return paginated list of objects.

        When :py:attr:`~.MultipleObjectMixin.items_per_page` is ``0``, this
        method will return the complete list.

        :return:
            A ``list`` of objects.

        """
        if not self.items_per_page:
            return self.get_filtered_queryset()

        start_index = (self.get_page_number() - 1) * self.items_per_page
        end_index = self.get_page_number() * self.items_per_page

        object_list = self.get_filtered_queryset()[start_index:end_index]

        if not len(object_list) and self.get_page_number() > 1:
            abort(404)
        else:
            return object_list

    def get_context_object_name(self):
        """
        Return the context object name.

        If :py:attr:`~.MultipleObjectMixin.context_object_name` is set, that
        value will be returned, else it will use the lowercased name of the
        document set in :py:attr:`~.MultipleObjectMixin.document_class` with
        ``_list`` suffix.

        :return:
            A ``str`` representing the object name.

        """
        if self.context_object_name:
            return self.context_object_name

        return '{0}_list'.format(self.document_class.__name__.lower())

    def get_context_data(self, **kwargs):
        """
        Return context data containing retrieved object list.

        :return:
            A ``dict`` containing the following keys:

            ``is_paginated``
                ``True`` if pagination is enabled, else ``False``.

            ``current_page_number``
                The current page number (``int``).

            ``total_page_count``
                The total number of pages (``int``).

            The key name containing the returned object list is generated
            by :py:meth:`.MultipleObjectMixin.get_context_object_name`.

        """
        kwargs.update({
            'is_paginated': self.items_per_page > 0,
            'current_page_number': self.get_page_number(),
            'total_page_count': self.get_page_count(),
            self.get_context_object_name(): self.get_paginated_object_list(),
        })
        return kwargs


class BaseListView(MultipleObjectMixin, View):
    """
    Base list view.

    This class inherits from:

    * :py:class:`.MultipleObjectMixin`
    * :py:class:`.View`

    This class implements all logic for retrieving a list of objects from the
    database, but does not implement rendering responses. See
    :py:class:`.ListView` for an usage example.

    """
    def get(self, *args, **kwargs):
        """
        Handler for GET requests.

        This retrieves the list of objects from the database and calls the
        ``render_to_response`` with the retrieved objects in the context
        data.

        :return:
            Ouput of ``render_to_response`` method implementation.

        """
        return self.render_to_response(self.get_context_data())


class ListView(TemplateResponseMixin, BaseListView):
    """
    List view for rendering a list of objects.

    This class inherits from:

    * :py:class:`.TemplateResponseMixin`
    * :py:class:`.BaseListView`

    This implements all logic for retrieving a list of objects from the
    database, including rendering a template.

    Usage example::

        class ArticleView(ListView):
            filter_fields = {
                'category': 'category',
            }
            items_per_page = 5
            document_class = Article
            template_name = 'article_list.html'

    """

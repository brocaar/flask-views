from __future__ import absolute_import

import json
from collections import Iterable

from pymongo.objectid import ObjectId

from flask_views.db.mongoengine.detail import BaseDetailView
from flask_views.json import JSONResponseMixin as JSONResponseMixinBase


class MongoengineEncoder(json.JSONEncoder):
    """
    Custom JSON encoder implementation for encoding Mongoengine documents.
    """
    def default(self, obj):
        if isinstance(obj, Iterable):
            out = {}
            for key in obj:
                out[key] = getattr(obj, key)
            return out

        if isinstance(obj, ObjectId):
            return unicode(obj)

        return json.JSONEncoder.default(self, obj)


class JSONResponseMixin(JSONResponseMixinBase):
    """
    Mixin class for rendering JSON responses out of Mongoengine documents.

    This class inherits from:

    * :py:class:`~flask_views.json.JSONResponseMixin`

    """
    encoder_class = MongoengineEncoder


class JSONDetailView(JSONResponseMixin, BaseDetailView):
    """
    Detail view for rendering JSON responses for a single object.

    This class inherits from:

    * :py:class:`~flask_views.db.mongoengine.json.JSONResponseMixin`
    * :py:class:`.BaseDetailView`

    Usage example::

        class ArticleView(JSONDetailView):
            get_fields = {
                'category': 'category',
                'slug': 'slug',
            }
            model_class = Article

    """
    def get_context_data(self):
        """
        Return the retrieved object.

        :return:
            :py:attr:`!JSONDetailView.object`.

        """
        return self.object

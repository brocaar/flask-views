Class types
===========

Mixin classes
-------------

Mixin classes provide a specialized set of functionality. Eg: rendering
a template, JSON encoding, fetching an object from the database. They can not
be used without the :py:class:`~flask_views.base.View` class.  


BaseView classes
----------------

BaseView classes (eg:
:py:class:`~flask_views.db.mongoengine.detail.BaseDetailView`) provide a full
set of logic, except the rendering of the response. This makes them highly
reusable. For example combined with the
:py:class:`~flask_views.json.JSONResponseMixin`, they can render JSON
responses, combined with the
:py:class:`~flask_views.base.TemplateResponseMixin`, they can render template
responses.

View classes
------------

View classes (eg: :py:class:`~flask_views.base.TemplateView`) provide a full
set of logic, including the rendering of responses.

Changelog
=========

0.2.1
-----

* Documentation improvements.
* Tests added to source distribution.


0.2
---

* :py:meth:`flask_views.base.TemplateResponseMixin.render_to_response` now
  accepts context data as ``context_data`` argument.
* :py:class:`flask_views.json.JSONResponseMixin` and
  :py:class:`flask_views.json.JSONView` classes added.
* :py:class:`flask_views.db.mongoengine.json.JSONResponseMixin` and
  :py:class:`flask_views.db.mongoengine.json.JSONDetailView` classes added.
* :py:mod:`!unittest2` used for testing under Python < 2.7.
* Fix: README.rst and LICENSE included in package.


0.1
---

* Initial release.

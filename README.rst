Flask-Views
===========

*Flask-Views* is a Flask extension which provides a set of class-based views,
based on the Django class based views.

Features:

* Base views for rendering templates and (JSON) responses, dispatched by HTTP
  request method
* Edit views for handling form submission (without database backend)
* Database views
    A set of views with database integration. Currently, only MongoDB (by
    using the Mongoengine module) is implemented.

    * Detail views for rendering a single object within a template or
      (JSON) response
    * Edit views for creating and updating items

Documentation
-------------

See: http://packages.python.org/Flask-Views/

Flask-Views
===========

*Flask-Views* is a Flask extension which provides a set of class based views,
inspired by Django.

Features:

* Base views for rendering templates and responses based on HTTP request method
* Edit views for handling form submission (without database backend)
* Database views
    A set of views with database integration. Currently, only MongoDB (by
    using the Mongoengine module) is implemented.

    * Detail views for rendering a single item on a page
    * Edit views for creating and updating items


Views
-----

.. toctree::
   :maxdepth: 5
   :glob:

   views/*
   views/db/index

Internals
---------

.. toctree::
    :maxdepth: 1

    tests/index

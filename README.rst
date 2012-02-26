Flask-Views
===========

*Flask-Views* is a Flask extension which provides a set of class-based views,
inspired by the Django class based views.

Currently this package contains a set of views for rendering (template
and JSON) responses dispatched by HTTP request method, views for handling
(`WTForms <http://wtforms.simplecodes.com/>`_) form submission and a collection
of database views for creating and updating objects (currently
`MongoDB <http://mongodb.org/>`_ is supported by using
`Mongoengine <http://mongoengine.org/>`_).

Installation
------------

*Flask-Views* can be installed by executing ``pip install flask-views``. The
source is available at: http://github.com/brocaar/flask-views

Examples
--------

Contact form
~~~~~~~~~~~~

::

    from flask_views.edit import FormView

    class ContactFormView(FormView):
        # For creating forms classes, see the WTForms documentation
        form_class = ContactForm 
        template_name = 'contact_form.html'

        def form_valid(self, form):
            # Do something with the submitted form data
            return super(ContactFormView, self).form_valid(form)

        def get_success_url(self):
            return url_for('contact.form')

    app.add_url_rule(
        '/contact/',
        view_func=ContactFormView.as_view('contact')
    )


Article view
~~~~~~~~~~~~

::

    from flask_views.db.mongoengine.detail import DetailView

    class ArticleView(DetailView):
        get_fields = {
            'category': 'category',
            'slug': 'slug',
        }
        # For creating document classes, see the Mongoengine documentation
        document_class = Article
        template_name = 'article_detail.html'

    app.add_url_rule(
        '/articles/<category>/<slug>/',
        view_func=ArticleView.as_view('article')
    )


Links
-----

* `Documentation <http://packages.python.org/Flask-Views/>`_
* `GitHub <http://github.com/brocaar/flask-views/>`_
* `Development version <http://github.com/brocaar/flask-views/zipball/master#egg=Flask-Views-dev>`_

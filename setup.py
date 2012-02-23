from setuptools import setup


setup(
    name='Flask-Views',
    version='0.2',
    url='http://github.com/brocaar/flask-views',
    license='BSD',
    author='Orne Brocaar',
    author_email='info@brocaar.com',
    description='Class based views for Flask',
    long_description=open('README.rst').read(),
    packages=[
        'flask_views',
        'flask_views.db',
        'flask_views.db.mongoengine',
    ],
    install_requires=[
        'Flask',
    ],
    tests_require=[
        'mock',
        'wtforms',
        'mongoengine',
        'unittest2',
    ],
    test_suite='flask_views.tests.suite',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

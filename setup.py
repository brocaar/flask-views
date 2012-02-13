from setuptools import setup


setup(
    name='Flask-Views',
    version='0.1dev',
    url='http://brocaar.com/',
    license='BSD',
    author='Orne Brocaar',
    author_email='info@brocaar.com',
    description='Class based views for Flask',
    long_description=open('README').read(),
    packages=[
        'flask_views',
        'flask_views.db',
        'flask_views.db.mongoengine',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

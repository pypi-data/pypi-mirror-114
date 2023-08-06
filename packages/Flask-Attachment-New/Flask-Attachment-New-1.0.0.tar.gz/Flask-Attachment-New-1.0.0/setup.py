"""
Flask-Logging
-------------
 
Log every request to specific view
"""
from setuptools import setup
 
setup(
    name='Flask-Attachment-New',
    version='1.0.0',
    url='http://iotwonderful.com',
    license='BSD',
    author='zhangchi, lisichen',

    description='attachment file',
    long_description=__doc__,
    packages=['flask_attachment'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask','Pillow'
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
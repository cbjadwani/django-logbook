# -*- coding: utf-8; mode: python; -*-
"""
A package that implements new logbook logging facilitites for
Django Web Framework.
(C) 2011 oDesk www.oDesk.com
"""

from setuptools import setup

setup(
    name='django_logbook',
    version='0.0.0',
    description='A package that implements new logbook logging facilities ' + \
                'for Django',
    long_description='A package that implements new logbook logging ' + \
                     'facilities for Django Web Framework',
    license='BSD',
    keywords='django logbook logging',
    url='https://github.com/cbjadwani/django_logbook',
    author='oDesk, www.odesk.com',
    author_email='developers@odesk.com',
    packages=['django_logbook'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])

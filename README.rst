===========
Information
===========

django-logbook is logbook plugin for Django Web Framework which adds new logging facilities to it.

============
Installation
============

Add next lines to your settings.py::

 import logging
 import logbook
 
 LOG_LEVEL_DB_HANDLER = logbook.INFO
 LOG_LEVEL_MAIL_HANDLER = logbook.ERROR
 LOG_LEVEL_LOGGING_GLOBAL = logging.ERROR

Don't forget to add 'django_logbook' to INSTALLED_APPS tuple.

Run::

 python manage.py syncdb

Or if you use south run::

 python manage.py migrate

==========
How to use
==========

For example we have file app/views.py, add next lines into it::

 import logbook

 logging = logbook.Logger('app.views')

After this you can log anything you want to django-logbook database::

 logging.error("Auth failed")
 logging.info("Have a nice day")



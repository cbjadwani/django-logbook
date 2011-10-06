===========
Information
===========

django_logbook is logbook plugin for Django Web Framework which adds new logging facilities to it.

============
Installation
============

Add next lines to your settings.py:

 import logging
 import logbook
 
 LOG_LEVEL_DB_HANDLER = logbook.INFO
 LOG_LEVEL_LOGGING_GLOBAL = logging.ERROR

Run::

 python manage.py syncdb

Or if you use south run::

 python manage.py migrate


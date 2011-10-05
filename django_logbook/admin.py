from django.contrib import admin
from django_logbook.models import Log, LogSummary


admin.site.register(Log)
admin.site.register(LogSummary)

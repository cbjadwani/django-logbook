import datetime
import logbook

from django.db import models
from django.conf import settings
from django.utils.hashcompat import md5_constructor

LOGBOOK_LEVELS = {
    'NOTSET': logbook.NOTSET,
    'DEBUG': logbook.DEBUG,
    'INFO': logbook.INFO,
    'WARNING': logbook.WARNING,
    'ERROR': logbook.ERROR,
    'CRITICAL': logbook.CRITICAL,
}

LEVEL_CHOICES = [(val, name) for (name, val) in LOGBOOK_LEVELS.items()]
LEVEL_CHOICES_DICT = dict(LEVEL_CHOICES)
HEADLINE_LENGTH = 60


class LogSummary(models.Model):
    "A summary of the log messages"
    checksum = models.CharField(max_length=32, primary_key=True)
    level = models.PositiveIntegerField(choices=LEVEL_CHOICES, default=logbook.ERROR, blank=True, db_index=True)
    source = models.CharField(max_length=128, blank=True, db_index=True)
    host = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    earliest = models.DateTimeField(default=datetime.datetime.now, db_index=True)
    latest = models.DateTimeField(default=datetime.datetime.now, db_index=True)
    hits = models.IntegerField(default=0, null=False)
    headline = models.CharField(max_length=HEADLINE_LENGTH, default='', blank=True)
    latest_msg = models.TextField()
    summary_only = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Log Summary'
        verbose_name_plural = 'Log Summaries'
        ordering = ['-latest']
        app_label = 'django_logbook'

    def __unicode__(self):
        return u"<LOGSUMMARY %s %s %s %s>" % (LEVEL_CHOICES_DICT.get(self.level, 'UNKNOWN'), self.host, self.source, self.headline)

    ## Admin methods

    def abbrev_msg(self, maxlen=500):
        if len(self.latest_msg) > maxlen:
            return u'%s ...' % self.latest_msg[:maxlen]
        return self.latest_msg
    abbrev_msg.short_description = u'Most recent msg'

    def latest_fmt(self):
        return self.latest.strftime('%Y%m%d\nT%H%m')
    latest_fmt.short_description = 'Latest'

    def earliest_fmt(self):
        return self.earliest.strftime('%Y%m%d\nT%H%m')
    earliest_fmt.short_description = 'Earliest'


class Log(models.Model):
    "A log message, used by LogbookDjangoDatabaseHandler"
    datetime = models.DateTimeField(default=datetime.datetime.now, db_index=True)
    level = models.PositiveIntegerField(choices=LEVEL_CHOICES, default=logbook.ERROR, blank=True, db_index=True)
    msg = models.TextField()
    source = models.CharField(max_length=128, blank=True, db_index=True)
    host = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    summary = models.ForeignKey(LogSummary, related_name='logs', blank=True, null=True, db_index=True)

    class Meta:
        ordering = ['-datetime']
        app_label = 'django_logbook'

    def __unicode__(self):
        return u"<LOG %s %s %s %s>" % (LEVEL_CHOICES_DICT.get(self.level, 'UNKNOWN'), self.host, self.source, self.get_headline())

    ## Admin methods

    def abbrev_msg(self, maxlen=500):
        if len(self.msg) > maxlen:
            return u'%s ...' % self.msg[:maxlen]
        return self.msg
    abbrev_msg.short_description = u'abbreviated msg'

    class Meta:
        get_latest_by = 'datetime'

    def datetime_fmt(self):
        return self.datetime.strftime('%Y%m%d\nT%H%m')
    datetime_fmt.short_description = 'Time'

    ## Methods for creating LogSummary

    def get_headline(self):
        return self.msg.split('\n')[0][:HEADLINE_LENGTH]

    def get_checksum(self):
        checksum = md5_constructor(str(self.level))
        checksum.update(self.source)
        checksum.update(self.host or '')
        checksum.update(self.get_headline())
        checksum = checksum.hexdigest()
        return checksum


## Signals

def summary_deleted_callback(sender, **kwargs):
    "When summary deleted, delete matching child logs"
    summary = kwargs['instance']
    Log.objects.filter(summary=summary).delete()
    return


def log_saved_callback(sender, **kwargs):
    "When a log is saved, add it to the summary"
    newlog = kwargs['instance']
    created = kwargs['created']
    if created:
        defaults = {'level': newlog.level,
                    'source': newlog.source,
                    'host': newlog.host,
                    'headline': newlog.get_headline(),
                    'earliest': newlog.datetime,
                    'summary_only': False}
        (summary, _) = LogSummary.objects.get_or_create(checksum=newlog.get_checksum(),
                                                        defaults=defaults
                                                        )
        summary.latest = newlog.datetime
        summary.latest_msg = newlog.msg
        summary.hits += 1
        summary.save()
        if summary.summary_only:
            # Log.objects.filter(summary=summary).delete()
            newlog.delete()
        else:
            newlog.summary = summary
            newlog.save()
    return

models.signals.pre_delete.connect(summary_deleted_callback, sender=LogSummary)
models.signals.post_save.connect(log_saved_callback, sender=Log)


def init():
    import logging
    from logbook.compat import redirect_logging

    from django_logbook import handlers

    db_handler = handlers.LogbookDjangoDatabaseHandler(level=settings.LOG_LEVEL_DB_HANDLER)
    db_handler.push_application()

    redirect_logging()  # redirect stdlib logging to logbook

    # this should be done after redirect_logging to be effective
    root = logging.getLogger()
    root.setLevel(settings.LOG_LEVEL_LOGGING_GLOBAL)

init()

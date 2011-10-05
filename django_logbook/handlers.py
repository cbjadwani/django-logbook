import socket
import logbook

from django.conf import settings
from django.core.mail import send_mail


HOST = socket.gethostname()


class StringFormatterHandler(logbook.Handler, \
                            logbook.StringFormatterHandlerMixin):
    def __init__(self, *args, **kwargs):
        format_string = kwargs.pop('format_string', None)
        super(StringFormatterHandler, self).__init__(*args, **kwargs)
        if format_string:
            logbook.StringFormatterHandlerMixin.__init__(self, format_string)


class LogbookDjangoDatabaseHandler(logbook.Handler):
    def emit(self, record):
        from django_logbook.models import Log, LOGBOOK_LEVELS

        record.pull_information()

        if hasattr(record, 'module'):
            source = '%s (%s)' % (record.module, record.lineno)
        else:
            source = '[%s]' % record.channel

        Log.objects.create(source=source,
                           level=LOGBOOK_LEVELS[record.level_name],
                           msg=record.msg,
                           host=HOST)


class DjangoSendMailHandler(StringFormatterHandler):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(DjangoSendMailHandler, self).__init__(*args, **kwargs)

    def send_mail(self, records, reason):
        subject = 'FingersCrossedLog: %s %s' % (self.request.method, \
                                                self.request.get_full_path())

        body = 'Reason: %s' % reason
        body += '\n\nLogs:\n'
        body += '\n'.join(self.format(record) for record in records)

        send_mail(subject,
                  body,
                  settings.EMAIL_FROM,
                  settings.LOG_EMAIL_RECIPIENTS,
                  fail_silently=True)

    def emit(self, record):
        self.send_mail([record], '<NA>')

    def emit_batch(self, records, reason):
        self.send_mail(records, reason)


def get_fingers_crossed_mailhandler(request):
    django_send_mail_handler = DjangoSendMailHandler(
            request,
            level=settings.LOG_LEVEL_MAIL_HANDLER,
            format_string=settings.LOG_FORMAT_STRING
    )
    fingers_crossed_mailhandler = logbook.FingersCrossedHandler(
            handler=django_send_mail_handler,
            action_level=settings.LOG_ACTIONLEVEL_FINGERSCROSSED_HANDLER,
            bubble=True,
            reset=True
    )
    return fingers_crossed_mailhandler

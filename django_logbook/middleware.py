from django_logbook.handlers import get_fingers_crossed_mailhandler


class FingersCrossedLogMiddleware(object):
    def process_request(self, request):
        fingers_crossed_handler = get_fingers_crossed_mailhandler(request)
        request.fingers_crossed_handler = fingers_crossed_handler
        fingers_crossed_handler.push_thread()

    def process_response(self, request, response):
        fingers_crossed_handler = request.fingers_crossed_handler
        fingers_crossed_handler.pop_thread()
        return response

import logging

from django.http import HttpResponse

logger = logging.getLogger("HealthCheckMiddleware")


class HealthCheckMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "GET":
            if request.path == "/readiness" or request.path == "/readiness/":
                return self.readiness(request)
            elif request.path == "/health" or request.path == "/health/":
                return self.healthz(request)
        return self.get_response(request)

    def healthz(self, request):
        '''
        :param request:
        :return: Returns that the server is alive.
        '''
        return HttpResponse("OK")

    def readiness(self, request):
        '''
        Add more logic for readiness check
        :param request:
        :return: True
        '''
        return HttpResponse("OK")

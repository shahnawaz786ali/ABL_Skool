from django.utils import timezone
import datetime as dt

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.session['last_login'] = str(dt.datetime.now())

        response = self.get_response(request)

        if request.user.is_authenticated and 'last_login' in request.session:
            request.session['last_logout'] =  str(dt.datetime.now())
        return response
from django.utils.deprecation import MiddlewareMixin
from .models import RequestLog

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Extract request details
        method = request.method
        path = request.path
        query_string = request.META.get('QUERY_STRING', '')
        remote_ip = request.META.get('REMOTE_ADDR', '')
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else None

        # Create a log record in the database
        RequestLog.objects.create(
            method=method,
            path=path,
            query_string=query_string,
            remote_ip=remote_ip,
            user=user
        )


import logging
import time

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'

        logger.info(
            '[%s] %s %s — User: %s — %.2fms',
            response.status_code,
            request.method,
            request.path,
            user,
            duration * 1000,
        )

        return response

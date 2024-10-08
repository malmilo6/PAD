from datetime import datetime

from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache


class RequestCounterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get the current timestamp rounded to the nearest second
        current_timestamp = int(datetime.now().timestamp())
        cache_key = f"load_count_{current_timestamp}"

        # Increment the request count in cache
        load_count = cache.get(cache_key, 0) + 1
        cache.set(cache_key, load_count, timeout=1)

        print(f"Incoming request: {request.path}")

    @classmethod
    def get_current_load(cls):
        # Get the current load count for the last second
        current_timestamp = int(datetime.now().timestamp())
        cache_key = f"load_count_{current_timestamp}"
        return cache.get(cache_key, 0)
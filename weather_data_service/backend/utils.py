from concurrent.futures import ThreadPoolExecutor, TimeoutError
from rest_framework.exceptions import APIException


class TaskTimeout(APIException):
    status_code = 504
    default_detail = "The request took too long to process."
    default_code = 'task_timeout'


def timeout(seconds=5):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with ThreadPoolExecutor() as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    return future.result(timeout=seconds)
                except TimeoutError:
                    raise TaskTimeout()  # Raise task timeout exception if it exceeds the limit
        return wrapper
    return decorator

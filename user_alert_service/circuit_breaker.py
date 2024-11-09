import pybreaker
import logging
from functools import wraps
from django.http import JsonResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a Circuit Breaker class
class CircuitBreaker:
    def __init__(self):
        self.breaker = pybreaker.CircuitBreaker(
            fail_max=50,           # Number of failures before tripping
            reset_timeout=30      # Timeout period before attempting to reset
        )

    def call_service(self, func, *args, **kwargs):
        """Call the service function with Circuit Breaker logic."""
        return self.breaker.call(func, *args, **kwargs)

# Create a global CircuitBreaker instance
circuit_breaker = CircuitBreaker()

# Decorator function
def circuit_breaker_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return circuit_breaker.call_service(func, *args, **kwargs)
        except pybreaker.CircuitBreakerError:
            logger.error("Circuit breaker is open. Service call failed.")
            return JsonResponse({"error": "Service unavailable"}, status=503)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return JsonResponse({"error": "Internal server error"}, status=500)

    return wrapper

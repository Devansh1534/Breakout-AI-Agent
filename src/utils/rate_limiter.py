# src/utils/rate_limiter.py

import time

def rate_limiter(interval):
    """
    Decorator to add a delay between function calls for rate limiting.
    
    Args:
        interval (float): Time in seconds to wait between calls.

    Returns:
        function: Wrapped function with rate limiting applied.
    """
    def wrapper(func):
        def wrapped_func(*args, **kwargs):
            time.sleep(interval)
            return func(*args, **kwargs)
        return wrapped_func
    return wrapper

from functools import wraps
from time import time, sleep

from .exceptions import element_exceptions


def retry(f=None, timeout=30, interval=0.1):
    """
    When working with a responsive UI, sometimes elements are not ready at the very second you request it
    This wrapper will keep on retrying finding or interacting with the element until its ready
    """

    # This allows us to use '@retry' or '@retry(timeout=thing, interval=other_thing)' for custom times
    if f is None:
        def rwrapper(f):
            return retry(f, timeout, interval)
        return rwrapper

    @wraps(f)
    def wrapper(*args, **kwargs):
        # The wrapped function gets the optional arguments retry_timeout and retry_interval added
        retry_timeout = kwargs.pop('retry_timeout', timeout)
        retry_interval = kwargs.pop('retry_interval', interval)
        prep = kwargs.pop('prep', None)

        end_time = time() + retry_timeout

        while True:
            try:
                if prep is not None:
                    prep()
                return f(*args, **kwargs)
            except element_exceptions:
                if time() > end_time:
                    # timeout, re-raise the original exception
                    raise
                sleep(retry_interval)

    return wrapper

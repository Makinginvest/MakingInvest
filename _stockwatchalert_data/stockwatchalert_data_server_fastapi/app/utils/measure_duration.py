import asyncio
import timeit
from functools import wraps


def measure_duration(duration):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = timeit.default_timer()
            result = await func(*args, **kwargs)
            end_time = timeit.default_timer()
            execution_time = end_time - start_time
            await asyncio.sleep(duration - execution_time) if execution_time < duration else None
            return result, execution_time

        return wrapper

    return decorator

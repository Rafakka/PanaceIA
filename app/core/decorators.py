from functools import wraps
from app.core.data_cleaner import normalize_universal_input
import inspect

def normalize_input(func):
    """Automatically normalize input dictionaries for FastAPI endpoints."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if len(kwargs) == 1 and isinstance(list(kwargs.values())[0], dict):
            normalized_kwargs = {
                list(kwargs.keys())[0]: normalize_universal_input(list(kwargs.values())[0])
            }
        else:
            normalized_kwargs = {
                k: normalize_universal_input(v) for k, v in kwargs.items()
            }

        result = func(*args, **normalized_kwargs)
        if inspect.iscoroutine(result):
            return await result
        return result
    return wrapper
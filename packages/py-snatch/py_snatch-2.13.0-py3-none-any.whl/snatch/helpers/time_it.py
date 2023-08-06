from functools import wraps
from typing import Callable

import arrow
from loguru import logger


def time_it(f: Callable) -> Callable:
    @wraps(f)
    def wrapper(*args, **kwargs) -> Callable:
        from snatch import __version__

        logger.info(f"Starting Snatch. Installed Version: {__version__}")
        start_time = arrow.utcnow()
        data = f(*args, **kwargs)
        end_time = arrow.utcnow()
        delta = end_time - start_time
        data.timeit = str(delta)
        return data

    return wrapper

import time
import logging
from typing import Callable, TypeVar

logger = logging.getLogger(__name__)
T = TypeVar("T")


def with_retry(fn: Callable[[], T], max_attempts: int = 3, backoff_base: float = 2.0) -> T:
    last_error = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except Exception as e:
            last_error = e
            if attempt < max_attempts:
                wait = backoff_base ** attempt
                logger.warning(f"Attempt {attempt} failed: {e}. Retrying in {wait}s...")
                time.sleep(wait)
    raise RuntimeError(f"All {max_attempts} attempts failed") from last_error

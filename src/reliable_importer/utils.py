from contextlib import contextmanager
import logging
from time import perf_counter

logger = logging.getLogger(__name__)

@contextmanager
def logged_operation(operation: str):
    logger.info("Операція '%s' розпочата", operation)
    start = perf_counter()
    try:
        yield
    except Exception:
        logger.exception("Операція '%s' завершилася помилкою", operation)
        raise
    else:
        elapsed = perf_counter() - start
        logger.info("Операція '%s' успішно завершена за %.6f сек", operation, elapsed)
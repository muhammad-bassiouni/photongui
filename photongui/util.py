import logging
from threading import Thread
from functools import wraps


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(filename)s] %(levelname)s | %(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.disabled = True


def threaded(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t_handler = Thread(target=func, args=args, kwargs=kwargs)
        t_handler.daemon = True
        t_handler.start()
    return wrapper


import logging
import time
import datetime


def log(level=logging.INFO):
    logging.basicConfig(level=level)

    def decorator(obj):
        logger = logging.getLogger(obj.__name__)
        logger.setLevel(level)
        if isinstance(obj, type):

            def wrapper(*args, **kwargs):
                logger.log(level, f"The instance of class [{obj.__name__}] was created")
                return obj(*args, **kwargs)

            return wrapper

        else:

            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                result = obj(*args, **kwargs)
                end_time = time.perf_counter()
                duration = end_time - start_time

                logger.log(
                    level,
                    f"""Timestamp: {datetime.datetime.now()}
                    Function name: {obj.__name__}
                    Arguments: {args} {kwargs}
                    Result: {result}
                    Duration: {duration:.10f}s
                    """,
                )
                return result

            return wrapper

    return decorator


@log(logging.CRITICAL)
def lin(x, a, b):
    return a * x + b


if __name__ == "__main__":
    lin(3, a=2, b=3)
    print(type(lin))

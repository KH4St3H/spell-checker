import time


def benchmark(func):
    def wrapper(*args, **kwargs):
        t = time.time()
        response = func(*args, **kwargs)
        t = time.time() - t
        return (t, response)

    return wrapper

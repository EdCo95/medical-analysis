from typing import Callable


def retry_on_failure(tolerance: int = 3):

    def the_actual_decorator(func: Callable):

        def function_wrapper(*args, **kwargs):
            fails = 0
            while fails < tolerance:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    fails += 1
                    if fails > tolerance:
                        raise e

        return function_wrapper

    return the_actual_decorator

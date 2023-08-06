from traceback import format_exc
from weighting_platform.functions import logging_functions


def round_decorator(round_operator):
    """ Декоратор, оборачивающий оператора раунда взвешивания """
    def wrapper(*args, **kwargs):
        try:
            round_operator(*args, **kwargs)
        except:
            logging_functions.fix_round_fail(args[0].gdw, format_exc())
            pass
    return wrapper


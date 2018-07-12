from functools import wraps
from apistar import exceptions


def has_group(*groups):
    """verifica que el usuario pertenezca al menos a uno de
    los grupos permitidos, en caso de no pertenecer a ningun grupo
    retornara un error 403"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for group in kwargs['user'].groups:
                if group in groups[0]:
                    return func(*args, **kwargs)
            raise exceptions.Forbidden()
        return wrapper
    return decorator

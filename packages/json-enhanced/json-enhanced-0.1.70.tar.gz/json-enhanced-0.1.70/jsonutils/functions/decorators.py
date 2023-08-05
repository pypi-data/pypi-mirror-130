from functools import wraps


class dummy:
    pass


def catch_exceptions(func):
    """
    When applied on a function, prevent it from throwing exceptions, if argument 'fail_silently' is set to True (False by default)
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.get("fail_silently") is True:
            try:
                return func(*args, **kwargs)
            except Exception:
                return
        else:
            return func(*args, **kwargs)

    return wrapper


def return_str_or_datetime(func):
    """
    This decorator will be applied to the parse_datetime function,
    so that it returns strings in isoformat format whenever the
    return_string argument is set to True.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.get("return_string") is True:
            return func(*args, **kwargs).isoformat()
        else:
            return func(*args, **kwargs)

    return wrapper


def return_value_on_exception(value, exception):
    """
    When applied on a function, it will return `value` if selected `exception` is raised
    and argument `fail_silently` is passed as True.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if kwargs.get("fail_silently") is True:
                try:
                    return func(*args, **kwargs)
                except exception:
                    if (
                        selected_return_value := kwargs.get("value_on_exception", dummy)
                    ) is not dummy:
                        return selected_return_value
                    return value
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator


def return_native_types(func):
    """ """

    @wraps(func)
    def wrapper(self):
        res = func(self)
        if self._native_types:
            return res._data
        return res

    return wrapper

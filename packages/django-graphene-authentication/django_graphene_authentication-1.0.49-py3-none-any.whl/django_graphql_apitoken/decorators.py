import functools
from calendar import timegm
from datetime import timedelta, datetime
from typing import Callable, List, Union, Optional

from django.middleware import csrf
from graphene.utils.thenables import maybe_thenable



def refresh_expiration(delta: timedelta):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(cls, *args, **kwargs):
            def on_resolve(payload):
                payload.refresh_expires_in = (
                    timegm(datetime.utcnow().utctimetuple()) +
                    delta.total_seconds()
                )
                return payload

            result = f(cls, *args, **kwargs)
            return maybe_thenable(result, on_resolve)
        return wrapper
    return decorator


def csrf_rotation(enable: bool = True):
    """
    Rotate CSRF. Used for security reasons

    Copied from graphql-jwt

    :param enable:
    :return:
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(cls, root, info, *args, **kwargs):
            result = f(cls, root, info, **kwargs)
            if enable:
                csrf.rotate_token(info.context)
            return result
        return wrapper
    return decorator
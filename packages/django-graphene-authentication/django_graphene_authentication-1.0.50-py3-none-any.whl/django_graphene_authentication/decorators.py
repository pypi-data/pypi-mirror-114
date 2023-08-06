import functools
from calendar import timegm
from datetime import timedelta, datetime
from typing import Callable, List, Union, Optional
from django.utils.translation import gettext as _

from django.middleware import csrf
from graphene.utils.thenables import maybe_thenable

from django_graphene_authentication.conf import settings


def get_ensure_refresh_token_decorator(cookie_name: str):
    """

    :param cookie_name: name of the cookie containing the refresh token
    :return:
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(cls, root, info, refresh_token=None, *args, **kwargs):
            if refresh_token is None:
                refresh_token = info.context.COOKIES.get(cookie_name)
                if refresh_token is None:
                    raise ValueError(
                        _('Refresh token is required'),
                    )
            return f(cls, root, info, refresh_token, *args, **kwargs)
        return wrapper
    return decorator


def get_refresh_expiration_decorator(delta: timedelta):
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


def get_csrf_rotation_decorator(enable: bool = True):
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


refresh_expiration = get_refresh_expiration_decorator(settings.JWT_REFRESH_EXPIRATION_DELTA)
ensure_refresh_token = get_ensure_refresh_token_decorator(settings.JWT_REFRESH_TOKEN_COOKIE_NAME)
csrf_rotation = get_csrf_rotation_decorator(True)
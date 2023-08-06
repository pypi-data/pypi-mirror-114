import abc
from typing import List, Optional

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import AnonymousUser


__all__ = [
    'allow_any',
    'JSONWebTokenMiddleware',
]

from django_graphene_authentication.path import PathDict


def allow_any(info, jwt_allow_any_classes: List[type] = None, **kwargs):
    field = getattr(
        info.schema,
        f'{info.operation.operation.name.lower()}_type',
    ).fields.get(info.field_name)

    if field is None:
        return False

    graphene_type = getattr(field.type, 'graphene_type', None)

    return graphene_type is not None and issubclass(graphene_type, tuple(jwt_allow_any_classes))


def _authenticate(request) -> bool:
    """
    Authenticate the request
    :param request:
    :return: true if we need to authenticate the user via the standard "authenticate" django process, false otherwise
    """
    is_anonymous = not hasattr(request, 'user') or request.user.is_anonymous
    return is_anonymous and get_http_authorization(request) is not None


def get_http_authorization(request, token_authentication_header_name: str = None, jwt_auth_header_prefix: str = None):
    """
    Fetch the token from the http request by looking at the HTTP authorization section.

    :param request: request containing a token.
    :param token_authentication_header_name: name of the HTTP header we need to scout
    :param jwt_auth_header_prefix: domain of the token (e.g., jwt, bearer)
    :return: token that will be use to authenticate the request
    """
    auth = request.META.get(token_authentication_header_name, '').split()
    # auth is a string like "jwt askfhdfklghdjhdhdfòlhdo"
    prefix = jwt_auth_header_prefix

    return auth[1]


def get_authentication_token_in_graphql_argument(request, jwt_api_token_name: str = None, allow_argument: bool = True, **kwargs) -> Optional[str]:
    """
    Fetch the authentication toklen from the graphql arguments of this resolve mechanism

    :param request: request whose token we need to fetch
    :param jwt_api_token_name: name of the token we need to fetch
    :param allow_argument: true if we should scout the token in the arguments as wll
    :param kwargs:
    :return: token hat we need to use to authenticate the request, or None if the token could not be found
    """
    if allow_argument:
        # fetch the arguments of this resolve request
        input_fields = kwargs.get('input')

        if isinstance(input_fields, dict):
            kwargs = input_fields

        # fetch the token
        return kwargs.get(jwt_api_token_name)
    return None


class AbstractGraphQLAuthenticationMiddleware(abc.ABC):
    """
    A graphene GraphQL middleware that allows you to perform authentication on the request.
    Copied from graphql-jwt.

    The middleware keeps scanning from a token in the resolver arguments. If it finds it, it manually set
    the user. As soon as we exit from the authenticated section of the graphql query, the user is not authenmticated
    anymore.

    The middleware is **not extendable** and is used to authenticate single resolver elements.

    """

    def __init__(self):
        self.cached_allow_any = set()

        if self.jwt_allow_argument():
            self.cached_authentication = PathDict()

    def jwt_allow_argument(self) -> bool:
        return False

    def jwt_allow_any_handle(self, info, jwt_allow_any_classes: List[type], **kwargs):
        return allow_any(info, jwt_allow_any_classes=jwt_allow_any_classes, **kwargs)

    def jwt_allow_any_classes(self) -> List[type]:
        return []

    def jwt_api_token_name(self) -> str:
        return "access_token"

    def jwt_global_authenticate_in_graphql(self) -> bool:
        return settings.DJANGO_GRAPHQL_APITOKEN.JWT_GLOBAL_AUTHENTICATE_IN_GRAPHQL

    def jwt_global_graphql_user_field_name(self) -> str:
        return settings.DJANGO_GRAPHQL_APITOKEN.JWT_GLOBAL_GRAPHQL_USER_FIELD_NAME

    def authenticate_context(self, info, **kwargs):
        root_path = info.path[0]

        if root_path not in self.cached_allow_any:
            if self.jwt_allow_any_handle(info=info, jwt_allow_any_classes=self.jwt_allow_any_classes(), **kwargs):
                self.cached_allow_any.add(root_path)
            else:
                return True
        return False

    def resolve(self, next, root, info, **kwargs):
        context = info.context
        # fetch the token using the argument
        token_argument = get_authentication_token_in_graphql_argument(
            context,
            jwt_api_token_name=self.jwt_api_token_name(),
            allow_argument=self.jwt_allow_argument(),
            **kwargs
        )

        # look if we have an authentication in the arguments
        if self.jwt_allow_argument() and token_argument is None:
            # we look at the resolver generatiun this request. Note that in case of A -> B -> C, A -> D,
            # in B we successfully authenticated, such an authentication will not be present in D at all, since
            # A is not authenticated
            user = self.cached_authentication.parent(info.path)

            if user is not None:
                context.user = user

            elif hasattr(context, 'user'):
                if hasattr(context, 'session'):
                    context.user = get_user(context)
                    self.cached_authentication.insert(info.path, context.user)
                else:
                    context.user = AnonymousUser()

        # we have a token in the arguments. However we did not allow token arguments to be elaborated
        # and/or the authentication failed.What we need to do is to authenticate normally the user
        if ((_authenticate(context) or token_argument is not None) and
                self.authenticate_context(info, **kwargs)):

            # triers to authenticate the user
            user = authenticate(request=context, **kwargs)

            if user is not None:
                context.user = user

                if self.jwt_allow_argument():
                    self.cached_authentication.insert(info.path, user)

        if hasattr(context, "user") and context.user is not None and self.jwt_global_authenticate_in_graphql():
            setattr(context, self.jwt_global_graphql_user_field_name(), context.user)

        return next(root, info, **kwargs)


class JSONWebTokenMiddleware(AbstractGraphQLAuthenticationMiddleware):
    pass


import abc
import logging
from typing import List, Optional

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import AnonymousUser


__all__ = [
    'allow_any',
    'AbstractGraphQLAuthenticationMiddleware',
]

from django_graphene_authentication.path import PathDict
from django_graphene_authentication.utils import get_authentication_token_in_graphql_argument, \
    get_authentication_token_from_http_authorization


LOG = logging.getLogger(__name__)


def allow_any(info, jwt_allow_any_classes: List[type] = None, **kwargs):
    field = getattr(
        info.schema,
        f'{info.operation.operation.name.lower()}_type',
    ).fields.get(info.field_name)

    if field is None:
        return False

    graphene_type = getattr(field.type, 'graphene_type', None)

    return graphene_type is not None and issubclass(graphene_type, tuple(jwt_allow_any_classes))


def get_path_string(info) -> str:
    """
    :param info: graphql info object
    :return: string representation of the path
    """
    return '/'.join(map(lambda x: str(getattr(x, "key", f"{x}")), filter(lambda x: x is not None, reversed(info.path))))

def should_authenticate(request) -> bool:
    """
    Authenticate the request
    :param request:
    :return: true if we need to authenticate the user via the standard "authenticate" django process, false otherwise
    """
    is_anonymous = not hasattr(request, 'user') or request.user.is_anonymous
    return is_anonymous and get_authentication_token_from_http_authorization(request) is not None


class AbstractGraphQLAuthenticationMiddleware(abc.ABC):
    """
    A graphene GraphQL middleware that allows you to perform authentication on the request.
    Copied from graphql-jwt.

    When a graphql resolve call is invoked, the middleware looks for a token in the resolver arguments.
    If it finds it, it manually set the user.
    As soon as we exit from the authenticated section of the graphql query, the user is not authenmticated
    anymore.

    If the graphql subquery exists from the authenticated section, the user is not authenticated anymore.

    .. :example:
        we look at the resolver generatiun this request. Note that in case of A -> B -> C, A -> D,
        in B we successfully authenticated, such an authentication will not be present in D at all, since
        A is not authenticated

    To avoid this problem, consider setting JWT_GLOBAL_AUTHENTICATE_IN_GRAPHQL

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
        return settings.GRAPHENE_AUTHENTICATION_JWT_GLOBAL_AUTHENTICATE_IN_GRAPHQL

    def jwt_global_graphql_user_field_name(self) -> str:
        return settings.GRAPHENE_AUTHENTICATION_JWT_GLOBAL_GRAPHQL_USER_FIELD_NAME

    def authenticate_context(self, info, **kwargs) -> bool:
        root_path = info.path[0]

        if root_path not in self.cached_allow_any:
            if self.jwt_allow_any_handle(info=info, jwt_allow_any_classes=self.jwt_allow_any_classes(), **kwargs):
                self.cached_allow_any.add(root_path)
            else:
                return True
        return False

    def debug(self, info, message):
        LOG.debug(f"{get_path_string(info)}: {message}")

    def info(self, info, message):
        LOG.info(f"{get_path_string(info)}: {message}")

    def resolve(self, next, root, info, **kwargs):
        self.debug(info, "trying to authenticate the graphql resolver...")
        context = info.context
        authenticated = False

        # fetch the token using the argument
        self.debug(info, f"Is there {self.jwt_api_token_name()} as a graphql resolver argument?")
        token_argument = get_authentication_token_in_graphql_argument(
            context,
            jwt_api_token_name=self.jwt_api_token_name(),
            allow_argument=self.jwt_allow_argument(),
            **kwargs
        )
        self.debug(info, f"token_argument named {self.jwt_api_token_name()}: {token_argument is not None}")

        # TOKEN ARGUMENT NOT FOUND. Ok MAYBE WE HAVE ALREADY AUTHENTICATED IN THE PARENT
        if self.jwt_allow_argument() and token_argument is None:
            # we look at the resolver generatiun this request. Note that in case of A -> B -> C, A -> D,
            # in B we successfully authenticated, such an authentication will not be present in D at all, since
            # A is not authenticated
            self.debug(info, f"token argument {self.jwt_api_token_name()} not found.")
            user = self.cached_authentication.parent(info.path)

            if user is not None:
                self.debug(info, f"Using as \"user\" the parent user resolver, namely {user}")
                context.user = user
                authenticated = True
            elif hasattr(context, 'user'):
                if hasattr(context, 'session'):
                    self.debug(info, f"while scanning for a user in this authentication resolution, we detected that we are using sessions and that the already sessioned user {context.user}. Use it")
                    context.user = get_user(context)
                    self.cached_authentication.insert(info.path, context.user)
                    authenticated = True
                else:
                    self.debug(info, f"User {user} is not presents in the session. Overwrite to AnonymousUser")
                    context.user = AnonymousUser()

        if not authenticated and should_authenticate(context) and self.authenticate_context(info, **kwargs):
            # Using the parent authentication failed. ok, let's try to authenticate the user by invoking django infrastructure
            # Let's we have a token in the arguments. However we did not allow token arguments to be elaborated
            # and/or the authentication failed.What we need to do is to authenticate normally the user

            # tries to authenticate the user.
            self.debug(info, f"trying to authenticate using standard django auth mechanisms...")
            if hasattr(context, "user"):
                authenticated = True
                if self.jwt_allow_argument():
                    self.cached_authentication.insert(info.path, user)
            else:
                user = authenticate(request=context, **kwargs)
                if user is not None:
                    authenticated = True
                    context.user = user
                    if self.jwt_allow_argument():
                        self.cached_authentication.insert(info.path, user)

        if authenticated and hasattr(context, "user") and context.user is not None and not context.user.is_anonymous and self.jwt_global_authenticate_in_graphql():
            self.info(f"Saving the request globally available user {context.user}")
            setattr(context, self.jwt_global_graphql_user_field_name(), context.user)

        # every other authentication method failed. If jwt_global_authenticate_in_graphql is set, use it
        if self.jwt_global_authenticate_in_graphql() and hasattr(context, self.jwt_global_graphql_user_field_name()) and (context.user is None or context.user.is_anonymous):
            previous_user = getattr(context, self.jwt_global_graphql_user_field_name())
            self.info(info, f"""we tried to authenticate the resolver, but the only way to do so was to reuse
                a previous globally-saved authenticated user ({previous_user}) in this grahql query plan.""")
            context.user = previous_user

        return next(root, info, **kwargs)


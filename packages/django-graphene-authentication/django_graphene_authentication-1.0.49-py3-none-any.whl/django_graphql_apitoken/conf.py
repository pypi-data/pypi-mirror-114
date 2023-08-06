import os
from datetime import timedelta
from typing import Optional, Callable, List

from django.conf import settings
from appconf import AppConf
from graphql_jwt.refresh_token.models import RefreshToken


class DjangoGraphQLApiTokenAppConf(AppConf):
    class Meta:
        prefix = "DJANGO_GRAPHQL_APITOKEN"
        #holder = "django_app_graphql.conf.settings"

    # graphql mutation comnfioguration-sk

    JWT_ACCESS_TOKEN_NAME: str = "access_token"
    """
    Token that is injected as input in the authentication bvackend
    """
    JWT_API_TOKEN_NAME: str = "api_token"
    """
    Token that is put as oputput of the authentication backend
    """

    JWT_PAYLOAD_NAME: str = "payload"

    JWT_REFRESH_EXPIRES_IN: str = "refresh_expires_in"

    JWT_GENERATED_TOKEN_NAME: str = "token"

    JWT_LONG_RUNNING_REFRESH_TOKEN_NAME: str = "refresh_token"

    JWT_LONG_RUNNING_REFRESH_TOKEN: bool = False

    JWT_ALLOW_REFRESH: bool = True

    JWT_AUDIENCE: Optional[str] = None

    JWT_ISSUER: Optional[str] = None

    JWT_ALGORITHM: str = "HS256"

    JWT_SECRET_KEY: str = settings.SECRET_KEY

    JWT_PUBLIC_KEY: Optional[str] = None

    JWT_PRIVATE_KEY: Optional[str] = None

    JWT_REUSE_REFRESH_TOKENS: bool = False

    JWT_REFRESH_TOKEN_MODEL: type = RefreshToken

    jwt_TOKEN_EXPIRATION_TIME: timedelta = timedelta(minutes=30)

    JWT_CSRF_ROTATION: bool = False

    # authentication middle configuration

    JWT_ALLOW_ARGUMENT: bool = True

    JWT_ALLOW_ANY_HANDLER: Optional[Callable] = None

    JWT_ALLOW_ANY_CLASSES: List[type] = []

    JWT_AUTH_HEADER_NAME: str = "HTTP_AUTHORIZATION"

    JWT_AUTH_HEADER_PREFIX: str = "JWT"

    JWT_GLOBAL_AUTHENTICATE_IN_GRAPHQL: bool = True
    """
    If true, the authentication middleware will also set JWT_GLOBAL_GRAPHQL_USER_FIELD_NAME in the graphql context.
    Useful if you klnow that during a graphql m,utation/query, there is only one authentication performed and you want
    to use that thrgouhout all the query resolvers.
    """

    JWT_GLOBAL_GRAPHQL_USER_FIELD_NAME: str = "authenticated_user"
    """
    Field name of the request that will dynamically be set if JWT_GLOBAL_AUTHENTICATE_IN_GRAPHQL is set
    """


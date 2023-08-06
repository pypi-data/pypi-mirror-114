import abc
from typing import Set, Optional, Dict

import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission
from jwt import exceptions as jwt_exceptions, DecodeError
from django.apps import apps
from django.conf import settings
from django.http import HttpRequest
from django_koldar_utils.django.AbstractDjangoBackend import AbstractDjangoBackend, TUSER, TPERMISSION, TUSER_ID

from django_graphene_authentication.utils import get_authenticating_token


class AbstractAuthenticateViaAccessToken(AbstractDjangoBackend[any, any, Permission]):
    """
    A backend that uses an access_token to authenticate the user.

    This backend enters in action when the Json
    If the user inject an access_token, what we need to do is to authenticate the user.

    Note that request is a standard http request where "are_we_authenticating_from_login_mutation" is set if we
    are trying to authenticate from the graphql login mutation of this package.
    Furthermore, if we have already authenticated and "JWT_GLOBAL_AUTHENTICATE_IN_GRAPHQL" is set, then
    """

    def authenticate(self, request, **kwargs) -> Optional[TUSER]:
        if request is None:
            return None
        if not getattr(request, 'are_we_authenticating_from_login_mutation', False):
            # we want to authenticate ONLY if we are inside the authentication mutation.
            return None

        # fetch the token
        token = get_authenticating_token(
            request=request,
            jwt_auth_header_prefix=self.jwt_auth_heder_prefix(),
            token_authentication_header_name=self.jwt_auth_header_name(),
            jwt_graphql_token_argument_name=self.jwt_access_token_name(),
            allow_argument=self.jwt_allow_argument(),
            **kwargs
        )
        if token is None:
            return None

        payload = self._get_payload(token, request, **kwargs)
        user = self._get_user_by_payload(payload, request, **kwargs)
        self.do_after_user_authenticated(request, token, user, payload, **kwargs)

        return user

    def get_user(self, user_id: TUSER_ID) -> Optional[TUSER]:
        User: type = get_user_model()
        return User.objects.get(pk=user_id)

    @abc.abstractmethod
    def do_after_user_authenticated(self, request: HttpRequest, authenticating_token: str, user: any, payload: any, **kwargs):
        """
        Code called each time an authenticatng token is used to authenticate a new user

        :param request: http request
        :param authenticating_token: token used to autrhentication
        :param user: authenticated user
        :param payload: decoded token
        :param kwargs: graphql args
        :return:
        """

        pass

    def jwt_allow_argument(self) -> bool:
        """
        If set, we can fetch the token from the graphql mutaiton arguments as well.
        :return:
        """
        return True

    @abc.abstractmethod
    def jwt_access_token_name(self) -> str:
        """
        Name of the token to expect as a graphql argument
        :return:
        """
        pass

    def jwt_access_token_public_key(self) -> Optional[str]:
        pass

    def jwt_access_token_private_key(self) -> Optional[str]:
        return None

    def jwt_access_token_secret_key(self) -> Optional[str]:
        return None

    def jwt_access_token_verify_expiration(self) -> bool:
        return True

    def jwt_access_token_verify(self) -> bool:
        return True

    def jwt_access_token_leeway(self) -> int:
        return 0

    def jwt_access_token_audience(self) -> Optional[str]:
        return None

    def jwt_access_token_issuer(self) -> Optional[str]:
        return None

    def jwt_access_token_algorithm(self) -> Optional[str]:
        return "HS256"

    def jwt_auth_header_name(self) -> str:
        return "HTTP_AUTHORIZATION"

    def jwt_auth_heder_prefix(self):
        return "JWT"

    def jwt_decode_handle(self, token, request: HttpRequest, **kwargs):
        if self.jwt_access_token_public_key() is None and self.jwt_access_token_secret_key() is None:
            raise jwt.DecodeError(f"Cannot decode token. You need to configure either jwt_access_token_public_key or jwt_access_token_secret_key to be non None!")
        return jwt.decode(
            token,
            self.jwt_access_token_public_key() or self.jwt_access_token_secret_key(),
            options={
                'verify_exp': self.jwt_access_token_verify_expiration(),
                'verify_aud': self.jwt_access_token_audience() is not None,
                'verify_signature': self.jwt_access_token_verify(),
            },
            leeway=self.jwt_access_token_leeway(),
            audience=self.jwt_access_token_audience(),
            issuer=self.jwt_access_token_issuer(),
            algorithms=[self.jwt_access_token_algorithm()],
        )

    def jwt_expired_token_detected(self, token, request: HttpRequest, **kwargs):
        raise jwt_exceptions.ExpiredSignatureError(f"token {token} is expired")

    def jwt_decode_error_detected(self, token, request: HttpRequest, **kwargs):
        raise jwt_exceptions.ExpiredSignatureError(f"token {token} cannot be decoded. Usually this is because you have written the wrong symmetric/asymmetric keys or if the algorithm chosen differs from the source of the token")

    def jwt_invalid_token_detected(self, token, request: HttpRequest, **kwargs):
        raise jwt_exceptions.DecodeError(f"{token} is invalid")

    def _get_payload(self, token: str, request: HttpRequest, **kwargs):
        """
        decode the token and fetch the payload

        :param token: token to decode
        :param request: http request
        :return:
        """
        payload = None
        try:
            payload = self.jwt_decode_handle(token, request, **kwargs)
        except jwt.ExpiredSignatureError:
            self.jwt_expired_token_detected(token, request, **kwargs)
        except jwt.DecodeError:
            self.jwt_decode_error_detected(token, request, **kwargs)
        except jwt.InvalidTokenError:
            self.jwt_invalid_token_detected(token, request, **kwargs)
        return payload

    @abc.abstractmethod
    def _get_user_by_payload(self, payload: any, request: HttpRequest, **kwargs) -> any:
        """
        fetch the user. You can override the method

        :param payload: decoded token
        :param request: http request
        :param kwargs: graphql args
        :return: user
        """
        pass

    def get_user_by_payload(self, payload: any, request: HttpRequest, **kwargs) -> any:
        """
        fetch the user from the payload. Youi should not override this method

        :param payload: decoded token
        :param request: http request
        :param kwargs: graphql params
        :return: user
        """
        try:
            user = self._get_user_by_payload(payload, request, **kwargs)
        except Exception:
            user = None

        if user is not None and not getattr(user, 'is_active', True):
            raise ValueError(f"User {user}is disabled")
        return user


class AbstractStandardAuthenticateViaAccessToken(AbstractAuthenticateViaAccessToken, ModelBackend):
    """
    After authenticating a user via an access token, we will the authorization fields (permissions)
    by polling the database as in django style. You only need to set the authentication token name
    """

    def do_after_user_authenticated(self, request: HttpRequest, authenticating_token: str, user: any, payload: any,
                                    **kwargs):
        pass

    def __init__(self):
        super(AbstractAuthenticateViaAccessToken, self).__init__()
        super(ModelBackend, self).__init__()

    def get_user_permissions(self, user_obj: TUSER, obj=None) -> Set[Permission]:
        return super(ModelBackend, self)._get_permissions(user_obj, obj, 'user')

    def get_group_permissions(self, user_obj: TUSER, obj=None) -> Set[Permission]:
        return super(ModelBackend, self)._get_permissions(user_obj, obj, 'group')

    def _get_user_by_payload(self, payload: any, request: HttpRequest, **kwargs) -> any:
        UserModel = get_user_model()
        user_id = payload["sub"]
        return UserModel._default_manager.get_by_natural_key(user_id)

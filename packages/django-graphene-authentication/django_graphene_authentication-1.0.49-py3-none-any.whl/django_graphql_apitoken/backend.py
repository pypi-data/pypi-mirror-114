import abc
from typing import Set, Optional, Dict

from django_koldar_utils.django.AbstactBackend import AbstractDjangoBackend, TUSER, TPERMISSION, TUSER_ID


class AuthenticateViaAccessToken(AbstractDjangoBackend):
    """
    A backend that uses an access_token to authenticate the user.
    """

    def authenticate(self, request, **kwargs) -> Optional[TUSER]:
        return None

    def get_user(self, user_id: TUSER_ID) -> Optional[TUSER]:
        pass

    def get_user_permissions(self, user_obj: TUSER, obj=None) -> Set[TPERMISSION]:
        pass

    def get_group_permissions(self, user_obj: TUSER, obj=None) -> Set[TPERMISSION]:
        pass


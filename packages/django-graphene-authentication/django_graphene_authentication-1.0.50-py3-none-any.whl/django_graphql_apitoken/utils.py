"""
Set of functions that are used both in the graphql graphene mutations/queries and in the graphene authentication
middleware
"""


# # imported from graphql-jwt
#
# from calendar import timegm
# from datetime import datetime
#
# import django
# from django.contrib.auth import get_user_model
# from django.utils.translation import gettext as _
#
# import jwt
#
#

#
#

#
#
# def jwt_decode(token, context=None):
#     return jwt.decode(
#         token,
#         jwt_settings.JWT_PUBLIC_KEY or jwt_settings.JWT_SECRET_KEY,
#         options={
#             'verify_exp': jwt_settings.JWT_VERIFY_EXPIRATION,
#             'verify_aud': jwt_settings.JWT_AUDIENCE is not None,
#             'verify_signature': jwt_settings.JWT_VERIFY,
#         },
#         leeway=jwt_settings.JWT_LEEWAY,
#         audience=jwt_settings.JWT_AUDIENCE,
#         issuer=jwt_settings.JWT_ISSUER,
#         algorithms=[jwt_settings.JWT_ALGORITHM],
#     )
#
#

#
#
# def get_credentials(request, **kwargs):
#     return (get_token_argument(request, **kwargs) or
#             get_http_authorization(request))
#
#
# def get_payload(token, context=None):
#     try:
#         payload = jwt_settings.JWT_DECODE_HANDLER(token, context)
#     except jwt.ExpiredSignatureError:
#         raise exceptions.JSONWebTokenExpired()
#     except jwt.DecodeError:
#         raise exceptions.JSONWebTokenError(_('Error decoding signature'))
#     except jwt.InvalidTokenError:
#         raise exceptions.JSONWebTokenError(_('Invalid token'))
#     return payload
#
#
# def get_user_by_natural_key(username):
#     UserModel = get_user_model()
#     try:
#         return UserModel._default_manager.get_by_natural_key(username)
#     except UserModel.DoesNotExist:
#         return None
#
#
# def get_user_by_payload(payload):
#     username = jwt_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER(payload)
#
#     if not username:
#         raise exceptions.JSONWebTokenError(_('Invalid payload'))
#
#     user = jwt_settings.JWT_GET_USER_BY_NATURAL_KEY_HANDLER(username)
#
#     if user is not None and not getattr(user, 'is_active', True):
#         raise exceptions.JSONWebTokenError(_('User is disabled'))
#     return user
#
#
# def refresh_has_expired(orig_iat, context=None):
#     exp = orig_iat + jwt_settings.JWT_REFRESH_EXPIRATION_DELTA.total_seconds()
#     return timegm(datetime.utcnow().utctimetuple()) > exp
#
#
# def set_cookie(response, key, value, expires):
#     kwargs = {
#         'expires': expires,
#         'httponly': True,
#         'secure': jwt_settings.JWT_COOKIE_SECURE,
#         'path': jwt_settings.JWT_COOKIE_PATH,
#         'domain': jwt_settings.JWT_COOKIE_DOMAIN,
#     }
#     if django.VERSION >= (2, 1):
#         kwargs['samesite'] = jwt_settings.JWT_COOKIE_SAMESITE
#
#     response.set_cookie(key, value, **kwargs)
#
#
# def delete_cookie(response, key):
#     response.delete_cookie(
#         key,
#         path=jwt_settings.JWT_COOKIE_PATH,
#         domain=jwt_settings.JWT_COOKIE_DOMAIN,
#     )

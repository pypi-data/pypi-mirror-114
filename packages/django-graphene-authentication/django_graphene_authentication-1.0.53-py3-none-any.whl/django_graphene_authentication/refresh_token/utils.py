from django.apps import apps
from django.conf import settings


def get_refresh_token_model():
    return apps.get_model(settings.JWT_REFRESH_TOKEN_MODEL)


def get_refresh_token_by_model(refresh_token_model, token, context=None):
    return refresh_token_model.objects.get(token=token, revoked__isnull=True)

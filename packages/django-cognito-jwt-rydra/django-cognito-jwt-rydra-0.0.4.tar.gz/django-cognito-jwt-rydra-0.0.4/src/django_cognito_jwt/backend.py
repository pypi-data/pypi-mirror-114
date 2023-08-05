import importlib
import logging
from sqlite3 import IntegrityError

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header)

from django_cognito_jwt.validator import TokenValidator, TokenError

logger = logging.getLogger(__name__)


def get_or_create_for_cognito(payload, access_token):
    cognito_id = payload['sub']

    user_model = get_user_model()

    try:
        return user_model.objects.get(cognito_id=cognito_id)
    except user_model.DoesNotExist:
        pass

    try:
        first_name = payload.get('given_name', None)
        last_names = [
            payload.get('middle_name', None),
            payload.get('family_name', None)
        ]
        last_name = ' '.join(filter(None, last_names)) or None

        user = user_model.objects.create(
            cognito_id=cognito_id,
            email=payload['email'],
            is_active=True,
            first_name=first_name,
            last_name=last_name)
    except IntegrityError:
        user = user_model.objects.get(cognito_id=cognito_id)

    return user


class JSONWebTokenAuthentication(BaseAuthentication):
    """Token based authentication using the JSON Web Token standard."""

    def __init__(self):
        self._jwt_validator = TokenValidator(
            settings.COGNITO_AWS_REGION,
            settings.COGNITO_USER_POOL,
            settings.COGNITO_API_SCOPE)

        super().__init__()

    def authenticate(self, request):
        """Entrypoint for Django Rest Framework"""
        jwt_token = self.get_jwt_token(request)
        if jwt_token is None:
            return None

        # Authenticate token
        try:
            jwt_payload = self._jwt_validator.validate(jwt_token)
        except TokenError:
            raise exceptions.AuthenticationFailed()

        try:
            user_function_import = settings.COGNITO_USER_CREATOR_FUNCTION
            module, func = user_function_import.rsplit('.', 1)
            module = importlib.import_module(module)
            user_function = getattr(module, func)
            user = user_function(jwt_payload, jwt_token)
            if user is None:
                raise exceptions.AuthenticationFailed("The user is not registered in the platform. Ask the administrator to sign you up")
        except Exception as e:
            if hasattr(settings, 'USE_FALLBACK') and settings.USE_FALLBACK:
                logger.warning(f'Could not use the user function authenticator, falling back to cognito. Reason: {str(e)}')
                user = get_or_create_for_cognito(jwt_payload, jwt_token)
            else:
                raise exceptions.AuthenticationFailed(str(e))

        return (user, jwt_token)

    def get_jwt_token(self, request):
        auth = get_authorization_header(request).split()
        if not auth or smart_text(auth[0].lower()) != 'bearer':
            return None

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

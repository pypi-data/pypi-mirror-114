import json

from decorator import decorator

import jwt
import redis
import requests
from django.conf import settings
from jwt.algorithms import RSAAlgorithm


class TokenError(Exception):
    pass


@decorator
def cached(func, *args, **kwargs):
    redis_client = redis.StrictRedis.from_url(settings.REDIS_URL)

    try:
        ser_jwt_data = redis_client.get('jwks')

        if not ser_jwt_data:
            jwt_web_keys = func(*args, **kwargs)
            redis_client.setex('jwks', 3600, json.dumps(jwt_web_keys))
        else:
            jwt_web_keys = json.loads(ser_jwt_data.decode('utf-8'))

        return jwt_web_keys
    except redis.exceptions.ConnectionError:
        return func(*args, **kwargs)


class TokenValidator:
    def __init__(self, aws_region, aws_user_pool, api_scope):
        self.aws_region = aws_region
        self.aws_user_pool = aws_user_pool
        self.api_scope = api_scope

    @property
    def pool_url(self):
        return 'https://cognito-idp.%s.amazonaws.com/%s' % (self.aws_region, self.aws_user_pool)

    @cached
    def _get_json_web_keys(self):
        response = requests.get(self.pool_url + '/.well-known/jwks.json')
        response.raise_for_status()

        json_data = response.json()
        jwt_web_keys = {item['kid']: json.dumps(item) for item in json_data['keys']}
        return jwt_web_keys

    def _get_public_key(self, token):
        try:
            headers = jwt.get_unverified_header(token)
        except jwt.DecodeError as exc:
            raise TokenError(str(exc))

        jwk_data = self._get_json_web_keys().get(headers['kid'])
        if jwk_data:
            return RSAAlgorithm.from_jwk(jwk_data)

    def validate(self, token):
        public_key = self._get_public_key(token)
        if not public_key:
            raise TokenError("No key found for this token")

        try:
            jwt_data = jwt.decode(
                token,
                public_key,
                issuer=self.pool_url,
                algorithms=['RS256'],
                options={'verify_aud': False}
            )

            if jwt_data['token_use'] != 'access' or self.api_scope not in jwt_data['scope'].split(' '):
                raise TokenError('Invalid scope')
        except (jwt.InvalidTokenError, jwt.ExpiredSignature, jwt.DecodeError) as exc:
            raise TokenError(str(exc))

        return jwt_data

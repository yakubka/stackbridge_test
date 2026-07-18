import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import User, BlacklistedToken


class JWTAuth(BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get('Authorization', '')
        if not header.startswith('Bearer '):
            return None
        token = header[7:]
        if BlacklistedToken.objects.filter(token=token).exists():
            raise AuthenticationFailed('token revoked')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.select_related('role').get(id=payload['user_id'], is_active=True)
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('token expired')
        except Exception:
            raise AuthenticationFailed('invalid token')

    def authenticate_header(self, request):
        return 'Bearer realm="api"'

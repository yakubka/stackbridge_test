import datetime
import jwt
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from ..authentication import JWTAuth
from ..models import User, BlacklistedToken


def make_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


class RegisterView(APIView):
    def post(self, request):
        d = request.data
        required = ('first_name', 'last_name', 'email', 'password', 'password2')
        if not all(k in d for k in required):
            return Response({'error': 'missing fields'}, status=400)
        if d['password'] != d['password2']:
            return Response({'error': 'passwords mismatch'}, status=400)
        if User.objects.filter(email=d['email']).exists():
            return Response({'error': 'email taken'}, status=400)
        user = User.objects.create(
            first_name=d['first_name'],
            last_name=d['last_name'],
            middle_name=d.get('middle_name', ''),
            email=d['email'],
            password=User.hash_password(d['password']),
        )
        return Response({'id': user.id}, status=201)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response({'error': 'invalid credentials'}, status=401)
        if not user.check_password(password):
            return Response({'error': 'invalid credentials'}, status=401)
        return Response({'token': make_token(user.id)})


class LogoutView(APIView):
    authentication_classes = [JWTAuth]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        BlacklistedToken.objects.get_or_create(token=request.auth)
        return Response({'ok': True})

from rest_framework.views import APIView
from rest_framework.response import Response

from ..authentication import JWTAuth
from ..models import User, TokenBlacklist


class ProfileView(APIView):
    authentication_classes = [JWTAuth]

    def _require_auth(self, request):
        if not hasattr(request.user, 'id'):
            return Response({'error': 'not authenticated'}, status=401)

    def get(self, request):
        err = self._require_auth(request)
        if err:
            return err
        u = request.user
        return Response({
            'id': u.id,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'middle_name': u.middle_name,
            'email': u.email,
            'role': u.role.name if u.role else None,
        })

    def patch(self, request):
        err = self._require_auth(request)
        if err:
            return err
        u = request.user
        for field in ('first_name', 'last_name', 'middle_name', 'email'):
            if field in request.data:
                setattr(u, field, request.data[field])
        if 'password' in request.data:
            u.password = User.hash_password(request.data['password'])
        u.save()
        return Response({'ok': True})

    def delete(self, request):
        err = self._require_auth(request)
        if err:
            return err
        u = request.user
        u.is_active = False
        u.save()
        TokenBlacklist.objects.get_or_create(token=request.auth)
        return Response({'ok': True})

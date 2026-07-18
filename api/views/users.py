from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from ..authentication import JWTAuth
from ..models import User, BlacklistedToken


class ProfileView(APIView):
    authentication_classes = [JWTAuth]
    permission_classes = [IsAuthenticated]

    def get(self, request):
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
        u = request.user
        for field in ('first_name', 'last_name', 'middle_name', 'email'):
            if field in request.data:
                setattr(u, field, request.data[field])
        if 'password' in request.data:
            u.password = User.hash_password(request.data['password'])
        u.save()
        return Response({'ok': True})

    def delete(self, request):
        u = request.user
        u.is_active = False
        u.save()
        BlacklistedToken.objects.get_or_create(token=request.auth)
        return Response({'ok': True})

from rest_framework.views import APIView
from rest_framework.response import Response

from ..authentication import JWTAuth
from ..permissions import IsAdmin
from ..models import AccessRule, Role, Resource

PERM_FIELDS = ('can_read', 'can_read_all', 'can_create', 'can_update', 'can_update_all', 'can_delete', 'can_delete_all')


def rule_to_dict(r):
    d = {'id': r.id, 'role': r.role.name, 'element': r.element.name}
    for f in PERM_FIELDS:
        d[f] = getattr(r, f)
    return d


class RulesView(APIView):
    authentication_classes = [JWTAuth]
    permission_classes = [IsAdmin]

    def get(self, request):
        rules = AccessRule.objects.select_related('role', 'element').all()
        return Response([rule_to_dict(r) for r in rules])

    def post(self, request):
        d = request.data
        try:
            role = Role.objects.get(name=d['role'])
            element = Resource.objects.get(name=d['element'])
        except (Role.DoesNotExist, Resource.DoesNotExist) as e:
            return Response({'error': str(e)}, status=404)
        rule, _ = AccessRule.objects.update_or_create(
            role=role, element=element,
            defaults={f: d.get(f, False) for f in PERM_FIELDS},
        )
        return Response({'id': rule.id}, status=201)


class RuleDetailView(APIView):
    authentication_classes = [JWTAuth]
    permission_classes = [IsAdmin]

    def patch(self, request, pk):
        try:
            rule = AccessRule.objects.get(pk=pk)
        except AccessRule.DoesNotExist:
            return Response({'error': 'not found'}, status=404)
        for f in PERM_FIELDS:
            if f in request.data:
                setattr(rule, f, request.data[f])
        rule.save()
        return Response({'ok': True})

    def delete(self, request, pk):
        AccessRule.objects.filter(pk=pk).delete()
        return Response({'ok': True})

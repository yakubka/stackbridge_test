from rest_framework.permissions import BasePermission

from .models import AccessRule


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        role = getattr(request.user, 'role', None)
        return bool(role and role.name == 'admin')


class HasPerm(BasePermission):
    element = None
    perm = 'can_read'

    def has_permission(self, request, view):
        if not hasattr(request.user, 'role') or not request.user.role:
            return False
        try:
            rule = AccessRule.objects.get(role=request.user.role, element__name=self.element)
            return getattr(rule, self.perm, False)
        except AccessRule.DoesNotExist:
            return False


def make_perm(element, perm='can_read'):
    return type('ElementPerm', (HasPerm,), {'element': element, 'perm': perm})

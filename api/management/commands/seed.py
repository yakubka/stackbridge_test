from django.core.management.base import BaseCommand

from api.models import Role, BusinessElement, AccessRule, User

ROLES = ['admin', 'manager', 'user', 'guest']
ELEMENTS = ['users', 'products', 'stores', 'orders', 'access_rules']

full = dict(can_read=True, can_read_all=True, can_create=True, can_update=True, can_update_all=True, can_delete=True, can_delete_all=True)
read_all = dict(can_read=True, can_read_all=True, can_create=False, can_update=False, can_update_all=False, can_delete=False, can_delete_all=False)
write_no_del = dict(can_read=True, can_read_all=True, can_create=True, can_update=True, can_update_all=False, can_delete=False, can_delete_all=False)
own_crud = dict(can_read=True, can_read_all=False, can_create=True, can_update=True, can_update_all=False, can_delete=True, can_delete_all=False)


class Command(BaseCommand):
    help = 'seed'

    def handle(self, *args, **kwargs):
        roles = {n: Role.objects.get_or_create(name=n)[0] for n in ROLES}
        els = {n: BusinessElement.objects.get_or_create(name=n)[0] for n in ELEMENTS}

        for el in els.values():
            AccessRule.objects.update_or_create(role=roles['admin'], element=el, defaults=full)

        for name in ('products', 'stores', 'orders'):
            AccessRule.objects.update_or_create(role=roles['manager'], element=els[name], defaults=write_no_del)

        for name in ('products', 'stores'):
            AccessRule.objects.update_or_create(role=roles['user'], element=els[name], defaults=read_all)
        AccessRule.objects.update_or_create(role=roles['user'], element=els['orders'], defaults=own_crud)

        for name in ('products', 'stores'):
            AccessRule.objects.update_or_create(role=roles['guest'], element=els[name], defaults=read_all)

        test_users = [
            ('Admin', 'Test', 'admin@test.com', 'admin123', 'admin'),
            ('Manager', 'Test', 'manager@test.com', 'manager123', 'manager'),
            ('User', 'Test', 'user@test.com', 'user123', 'user'),
            ('Guest', 'Test', 'guest@test.com', 'guest123', 'guest'),
        ]
        for fn, ln, email, pwd, role in test_users:
            if not User.objects.filter(email=email).exists():
                User.objects.create(first_name=fn, last_name=ln, email=email, password=User.hash_password(pwd), role=roles[role])

        self.stdout.write('done.')

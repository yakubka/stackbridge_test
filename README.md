# auth service

Backend authentication and authorization system built with Django REST Framework.

## Stack

- Python 3.10+, Django 4.2, DRF
- PostgreSQL
- PyJWT, bcrypt

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env

python manage.py migrate
python manage.py seed
python manage.py runserver
```

## Access control schema

### Tables

**roles** — user roles in the system.

| id | name    |
|----|---------|
| 1  | admin   |
| 2  | manager |
| 3  | user    |
| 4  | guest   |

**business_elements** — resources that access is controlled for.

| id | name         |
|----|--------------|
| 1  | users        |
| 2  | products     |
| 3  | stores       |
| 4  | orders       |
| 5  | access_rules |

**access_roles_rules** — permission matrix linking roles to elements.

| column         | type | meaning                                        |
|----------------|------|------------------------------------------------|
| role_id        | FK   | reference to roles                             |
| element_id     | FK   | reference to business_elements                 |
| can_read       | bool | read own records                               |
| can_read_all   | bool | read all records                               |
| can_create     | bool | create new records                             |
| can_update     | bool | update own records                             |
| can_update_all | bool | update any record                              |
| can_delete     | bool | delete own records                             |
| can_delete_all | bool | delete any record                              |

### Default access matrix

| role    | products        | stores          | orders                      |
|---------|-----------------|-----------------|-----------------------------|
| admin   | full access     | full access     | full access                 |
| manager | read, write     | read, write     | read, write                 |
| user    | read all        | read all        | own: read, create, delete   |
| guest   | read all        | read all        | none                        |

Only admin has access to users and access_rules elements.

## Endpoints

```
POST   /api/auth/register/
POST   /api/auth/login/
POST   /api/auth/logout/

GET    /api/me/
PATCH  /api/me/
DELETE /api/me/

GET    /api/admin/rules/
POST   /api/admin/rules/
PATCH  /api/admin/rules/<id>/
DELETE /api/admin/rules/<id>/

GET    /api/products/
GET    /api/stores/
GET    /api/orders/
```

All protected endpoints require `Authorization: Bearer <token>` header.

## Authentication flow

1. User registers or logs in, receives JWT token.
2. Token contains user_id, expires in 7 days.
3. Each request includes the token in Authorization header.
4. Custom JWTAuth class decodes the token and sets request.user.
5. On logout, token is added to blacklist table and rejected on subsequent requests.

## Test accounts

After running seed command.

| email             | password    | role    |
|-------------------|-------------|---------|
| admin@test.com    | admin123    | admin   |
| manager@test.com  | manager123  | manager |
| user@test.com     | user123     | user    |
| guest@test.com    | guest123    | guest   |

# auth service

```
api/
  models.py
  authentication.py
  permissions.py
  views/
    auth.py
    users.py
    admin.py
    mock.py
  management/commands/seed.py
```

```bash
cp .env.example .env
python manage.py migrate
python manage.py seed
python manage.py runserver
```

В `.env` нужно указать `DB_NAME` и `DB_PASSWORD` от локальной PostgreSQL базы. Создать её можно так:

```bash
psql -U postgres -c "CREATE DATABASE auth_db;"
```

Тогда `DB_NAME=auth_db`, `DB_PASSWORD` — пароль твоего postgres-пользователя (по умолчанию пустой если ставил без пароля).

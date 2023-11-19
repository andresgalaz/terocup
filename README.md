# terocup

## Superusuario

```text
admin/ZFzf2023
```

## Usuario Inicial

```text
nico_perez/cambiar_2023
```

## Comandos

```bash
psql -d django_db -h localhost -U agalaz -w
pg_dump -d django_db -h localhost -U agalaz -w > django_db.sql

./manage.py createsuperuser
./manage.py collectstatic
./manage.py makemigrations terocup
./manage.py migrate
./manage.py runserver 0.0.0.0:8002
./manage.py importa_csv carga_inicial/causas.csv
./manage.py changepassword ROCIOHERRERA
```

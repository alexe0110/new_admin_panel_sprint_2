Запуск БД

```bash
docker run -d \
  --name postgres \
  -p 5432:5432 \
  -v $HOME/postgresql/data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=123qwe \
  -e POSTGRES_USER=app \
  -e POSTGRES_DB=movies_database  \
  postgres:16
```

Подключится к БД

    psql -h 127.0.0.1 -U app -d movies_database 

## Запуск админки 

    make migrate
    python movies_admin/manage.py createsuperuser
    make run


#### Перевод

Сгенерировать *.po файлы со строками которые нужно перевести

    python manage.py makemessages -l en -l ru 
`msgid` — это кодовое название, которое вы назначили строке; <br>
`msgstr` — это перевод для этого языка.

Сгенерировать *.mo файлы, они для джанги

    python manage.py compilemessages -l en -l ru 

#### Миграции

Сгенеровать миграцию по описанным моделям

    python manage.py makemigrations movies --settings=config.settings

Применить миграцию 

    python movies_admin/manage.py migrate
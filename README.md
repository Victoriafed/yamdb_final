# yamdb_final
yamdb_final

# Api_YaMDb

## Описание
Проект YaMDb собирает отзывы пользователей на произведения.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
### Благодаря этому проекту пользователи смогут:
 - Зарегистрироваться
 - Оставить отзыв и оценку на произведение
 - Оставить комментарий к отзыву 
 - многое многое другое

### Шаблон наполнения env-файла,
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
### Запуск приложения в контейнерах
```
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --no-input
docker compose exec web python manage.py dumpdata > db1.json #резервная копия БД
docker cp db1.json <..> # перенос бд в контейнер 
docker compose exec web python manage.py loaddata db1.json
```

### Авторы 
- Федор Петринчук
- Виктория Федорова
- Артур Костенков

### Примеры запросов:
***Регистрация***
- POST: 
http://127.0.0.1:8000/api/v1/auth/signup/
```
{
    "email": "user@example.com",
    "username": "user1"
}
```

***Получение токена***
- POST: 
http://127.0.0.1:8000/api/v1/auth/token/
```
{
    "username": "user1",
    "confirmation_code": "string"
}
```
Результат
```
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc0NjgwNjkwLCJpYXQiOjE2NzQ1OTQyOTAsImp0aSI6IjYyOGUxODliZTZkZTRlMWNiMGQ5MThiMDkwYTIyMTk1IiwidXNlcl9pZCI6MX0.yZldqDRF2jhLzqbAcO4X4u7C3Bki63IRgFZilu8d0tc"
}
```
***Получение информации о произведении***
- GET: 
http://127.0.0.1:8000/api/v1/titles/1/
```
{
    "id": 1,
    "name": "Кот в сапогах",
    "year": 2023,
    "rating": 6,
    "description": "Мультфильм о коте",
    "genre": ["Мультфильм"],
    "category": {
        "name": "Для детей",
        "slug": "baby"
    }
}
```
***Получение списка всех отзывов на произведение***
- GET: 
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
        {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
        }
    ]
}
```

***Добавление нового отзыва на произведение***
- POST: 
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
#### Payload
```
{
    "text": "string",
    "score": 1
}
```
#### Response (200)
```
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
}
```
***Получение списка всех комментариев к отзыву***
- GET: 
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "text": "string",
            "author": "string",
            "pub_date": "2019-08-24T14:15:22Z"
        }
    ]
}
```
***Добавление комментария к отзыву***
- POST: 
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
#### Payload
```
{
  "text": "string"
}
```
#### Response (200)
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```


![Django-app workflow](https://github.com/Victoriafed/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

ВМ 158.160.50.23

superuser name:admin ps:admin

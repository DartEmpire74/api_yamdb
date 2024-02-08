# api_yamdb
api_yamdb
# YAMDB API

## О проекте

Данный проект является сервисом, на котором люди могут оставлять отзывы и оценки для произведений разных категорий и жанров, а именно: о книгах, фильмах, музыке и т.д., с возможностью комментирования каждого пользовательского отзыва.

# Стек проекта:

- Python 3.9.10
- Django 3.2
- Django REST Framework 3.12.4
- Simple-JWT
- SQlite
- Pytest

# Как запустить

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/DartEmpire74/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

### Для Linux

```
source venv/bin/activate
```

### Для Windows

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

# Документация по работе с API

Для того чтобы посмотреть какие запросы можно отправлять нужно запустить проект и потом в браузере открыть данный адрес:

```
http://127.0.0.1:8000/redoc/
```

## Примеры запросов 

### Categories
Пример `GET` запроса: http://yourdomain.com/api/v1/categories/

```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```

### Genres
Пример `GET` запроса: http://yourdomain.com/api/v1/genres/

```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```

### Titles

Пример `GET` запроса: http://yourdomain.com/api/v1/titles/

```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```

### Reviews

Пример `GET` запроса: http://yourdomain/api/v1/titles/{title_id}/reviews/

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
### Comments

Пример `GET` запроса: http://yourdomain/api/v1/titles/{title_id}/reviews/{review_id}/comments/

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

### Users

Пример `GET` запроса: http://yourdomain/api/v1/users/

```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "username": "string",
      "email": "user@example.com",
      "first_name": "string",
      "last_name": "string",
      "bio": "string",
      "role": "user"
    }
  ]
}
```


# Импорт данных из csv файлов.
В проекте реализован функционал импорта заранее подготовленных данных из csv файлов.
Для импорта необходимо использовать команду:

```
python manage.py import_from_csv "static/data/category.csv"
"static/data/genre.csv" "static/data/titles.csv" 
"static/data/genre_title.csv" "static/data/users.csv"
```


## Авторы проекта:
[Артем Бахарев](https://github.com/DartEmpire74) - Team lead

[Михаил Делянченко](https://github.com/MihaDemon)

[Артемьев Дмитрий](https://github.com/ArtemevD)

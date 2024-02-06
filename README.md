# YAMDB API

## О проекте

Данный проект является сервисом для оценки произведений разных категорий и жанров с возможностью комментирования каждого пользовательского отзыва

# Под капотом

В этом проекте используется Django версии 3.2 cовместно с библиотекой djangorestframework версии 3.12

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

# Пример работы с API

Для того чтобы посмотреть какие запросы можно отпровлять нужно запустить проект и потом в браузере открыть данный адрес:

```
http://127.0.0.1:8000/redoc/
```
# api_yamdb

### Проект YaTube

YaTube это небольшой блог с пользовательским интерфейсом(HTML, CSS). Проект реализован с помощью фреймворка Django.
Предусмотрена авторизация пользователей, добавление и редактирование записи, возможность оставлять
комментарии и подписываться на понравившихся авторов. Реализована фильтрация постов по авторам. Проект покрыт тестами (Unittest).

## Как развернуть проект

Системные требования:

- Python==3.7.9
- Django==2.2.16

1. Клонировать репозиторий

2. Установить виртуальное окружение

> python -m venv venv

3. Активировать виртуальное окружение

> source venv/scripts/activate

4. Обновить pip

> python -m pip install --upgrade pip

5. Установить зависимости

> pip install -r requirements.txt

6. Применить миграции

> python manage.py makemigrations

> python manage.py migrate

7. Запустить тестовый сервер

> python manage.py runserver

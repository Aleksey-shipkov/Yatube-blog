# api_yamdb

### Проект YaTube

Проект YaTube это учебный проект небольшого блога. 
Проект позволяет добавлять и редактировать записи, оставлять комментарии 
и подписываться на понравившивхся авторов. Проект реализован с помощью фреймворков Django и Bootstrap

## Как развернуть проект

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

## Пример Социальной сети на Django
- Регистрация и авторизация пользователей.
- Профили пользователей, редактирование профиля.
- Добавление, редактирование, отображение и удаление  постов.
- Запросы и добавления в друзья.
- Сообщения и чаты с использованием Websocket.

Технологии:
- Thumbnails.
- Ckeditor.
- Websockets.
- DRF.

### Начало работы:
#### 1. Установить зависимости:
>pip install -r requirements.txt

#### 2. Применить миграции и создать пользователя:
> python manage.py makemigrations \
> python manage.py migrate \
> python manage.py createsuperuser

#### 6. Запустить Django.
> python manage.py runserver

### Инструкции:
Начальная страница `http://localhost:8000/profile`
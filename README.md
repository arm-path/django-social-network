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
> python manage.py createsuperuser \
> python manage.py collectstatic

#### 6. Запустить Django.
> python manage.py runserver

### Внешний вид:
[Авторизации пользователя](README/images/login.png) \
[Регистрации пользователя](README/images/registration.png) \
[Отображение профиля пользователя](README/images/profile_detail.png)\
[Изменение профиля пользователя](README/images/profile_edit.png)\
[Отображение поста пользователя](README/images/post_detail.png) \
[Изменение поста пользователя](README/images/post_edit.png) \
[Отображение действий друзей](README/images/news.png) \
[Отображение списка диологов](README/images/chat_list.png) \
[Отображение чата](README/images/chat_detail.png)
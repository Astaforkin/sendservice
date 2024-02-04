### Sendservice
Cервис, который по заданным правилам запускает рассылку по списку клиентов.

### Технологии:
- Python
- Django
- Django Rest Framework
- Docker
- Celery

## Установка и запуск

1. Склонировать репозиторий с Github:

````

````
2. Перейти в директорию проекта

3. Создать виртуальное окружение:

````
python -m venv venv
````

4. Активировать окружение: 

````
source venv/bin/activate
````
 
5. Установка зависимостей:

```
pip install -r requirements.txt
```

6. Создать и применить миграции в базу данных:
```
python manage.py makemigrations
python manage.py migrate
```
7. Запустить сервер
```
python manage.py runserver
```
8. Запустить celery
```
celery -A sendservice worker -l info
```

## Установка проекта с помощью docker-compose


1. Склонировать репозиторий с Github
```
git clone git@github.com:Astaforkin/sendservice.git
```
2. Перейти в директорию проекта
3. Запустить контейнеры 
``` 
sudo docker compose up -d
 ```
4. Остановка работы контейнеров 
```
sudo docker compose stop
```


## Автор

[Астафоркин Никита](https://github.com/Astaforkin)
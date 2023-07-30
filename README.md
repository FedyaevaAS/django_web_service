# Проект: веб-сервис на базе django

### Функционал сервиса
* Принимает из POST-запроса .csv файлы для дальнейшей обработки;
* Обрабатывает типовые deals.csv файлы, содержащие истории сделок;
* Сохраняет извлеченные из файла данные в БД проекта;
* Возвращает обработанные данные в ответе на GET-запрос.

### Стек технологий Backend
- Python
- Django
- PostgreSQL
- nginx
- gunicorn
- Docker

### Начало работы
Клонируйте репозиторий и перейдите в него в командной строке:
```
git clone https://github.com/FedyaevaAS/django_web_service
```
```
cd django_web_service
```
### Запуск проекта локально
- Установите Docker, используя инструкции с официального сайта:
https://www.docker.com/products/docker-desktop/
- Создайте файл .env в корне проекта со следующим содержимым:
    ```
    SECRET_KEY=<> # Секретный ключ
    POSTGRES_DB=web_service_db # Название базы данных
    POSTGRES_USER=postgres  # Логин для подключения к базе данных
    POSTGRES_PASSWORD=postgres  # Пароль для подключения к базе данных
    DB_HOST=localhost  # Название сервиса (контейнера)
    DB_PORT=5432  # Порт для подключения к базе данных
    ```
- Перейдите в папку infra выполните команды для запуска приложения в контейнерах

    - Собрать и запустить контейнеры:
        ```
        docker-compose up -d --build
        ```
    - Выполнить миграции:
        ```
        docker-compose exec backend python manage.py migrate
        ```
    - Остановить контейнеры:
        ```
        docker-compose down -v 
        ```

### Доступные эндпоинты
GET:
http://127.0.0.1/api/top-clients/
POST:
http://127.0.0.1/api/upload/

Для того, чтобы протестировать POST запрос через Postman:
* Перейдите во вкладку Body и в разделе Body Type выберите form-data;
* В графе KEY введите file;
* В графе VALUE нажмите Select Files и выберите CSV файл, который хотите загрузить;
* Нажмите кнопку "Send" для выполнения запроса.

### Автор
Федяева Анастасия

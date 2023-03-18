# Shop Store
Построение интернет магазина на **Django**
#### **Стэк:**
- [Python](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- Django / Django REST Framework
- Celery
## Локальный запуск:star:
Все действия следует выполнять из исходного каталога проекта и только после установки всех требований.
1. Во-первых, создайте и активируйте новую виртуальную среду:
- ```cmd
  python3.9 -m venv ../venv
  source ../venv/bin/activate
  ```
2. Установить пакеты:
- ```cmd
  pip install --upgrade pip
  pip install -r requirements.txt
  ```
3. Запуск скрвера Redis:
- ```
  sudo service redis-server start
  ```
4. Запуск Celery:
 - ```
   celery -A store worker --loglevel=INFO
   ```
5. Запустите зависимости проекта, миграции, заполните базу данных данными фикстурами и т. д.:
- ```cmd
  python3 manage.py migrate
  python3 manage.py loaddata products/fixtures/categories.json
  python3 manage.py loaddata products/fixtures/goods.json
  python3 manage.py runserver 
  ```
Некоторые пункты могут отличаться в зависимости от вашей ОС.

markdown
# Система управления клиентами

Этот проект представляет собой систему управления клиентами, которая позволяет управлять клиентами и их номерами телефонов в базе данных PostgreSQL. Проект включает функции для добавления, обновления и удаления клиентов, а также поиска клиентов по различным критериям.

## Структура проекта

ClientManagementSystem/ 
├── client_management.py 
├── create_db.py 
├── db_utils.py 
├── validation.py
├── test_client_management.py 
├── config_template.py 
├── .env (не включен в репозиторий) 
└── README.md


## Требования

- Python 3.7+
- PostgreSQL
- Библиотека `python-dotenv`

## Настройка

1. Клонируйте репозиторий:

```
git clone https://github.com/yourusername/ClientManagementSystem.git
cd ClientManagementSystem
Создайте виртуальное окружение и активируйте его:


python -m venv .venv
source .venv/bin/activate  # Для Windows используйте `source .venv/Scripts/activate`
Установите необходимые пакеты:


pip install -r requirements.txt
Создайте файл .env в корневом каталоге проекта со следующим содержимым:

DATABASE_NAME=имя_вашей_базы_данных
DATABASE_USER=пользователь_вашей_базы_данных
DATABASE_PASSWORD=пароль_вашей_базы_данных
DATABASE_HOST=хост_вашей_базы_данных
DATABASE_PORT=порт_вашей_базы_данных
Заполните значения вашего файла .env.

Использование
Создайте структуру базы данных:


python create_db.py
Запустите тесты, чтобы убедиться, что все настроено правильно:


python -m unittest test_client_management.py
Файлы
client_management.py: Содержит функции для управления клиентами и их номерами телефонов.

create_db.py: Содержит функцию для создания структуры базы данных.

db_utils.py: Содержит утилиты для работы с базой данных.

validation.py: Содержит функции для проверки форматов электронной почты и номеров телефонов.

test_client_management.py: Содержит тесты для всех функций.

README.md: Документация проекта.

.env: Переменные окружения (не включен в репозиторий).

Функции
add_client(first_name, last_name, email): Добавляет нового клиента.

add_phone(client_id, phone_number): Добавляет номер телефона для существующего клиента.

update_client(client_id, first_name=None, last_name=None, email=None): Обновляет информацию о клиенте.

delete_phone(client_id, phone_number): Удаляет номер телефона для существующего клиента.

delete_client(client_id): Удаляет существующего клиента.

find_client(first_name=None, last_name=None, email=None, phone_number=None): Ищет клиента по его данным.

check_data(): Выводит всех клиентов и их номера телефонов.
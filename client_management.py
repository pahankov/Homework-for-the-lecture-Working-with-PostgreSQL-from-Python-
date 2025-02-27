import psycopg2
import re
from config import DATABASE

def get_connection():
    """
    Создает и возвращает соединение с базой данных.
    """
    return psycopg2.connect(**DATABASE)

def execute_query(query, params=None):
    """
    Выполняет SQL-запрос с переданными параметрами и возвращает результат.

    :param query: SQL-запрос для выполнения.
    :param params: Параметры для SQL-запроса.
    :return: Результат выполнения запроса.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if query.strip().upper().startswith("SELECT"):
                    return cur.fetchall()
                else:
                    conn.commit()
    except psycopg2.Error as e:
        print(f"Ошибка выполнения запроса: {e}")

def validate_email(email):
    """
    Проверяет, что адрес электронной почты имеет правильный формат.

    :param email: Адрес электронной почты.
    :return: True, если формат корректен, False в противном случае.
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_phone(phone_number):
    """
    Проверяет, что номер телефона содержит только цифры.

    :param phone_number: Номер телефона.
    :return: True, если номер корректен, False в противном случае.
    """
    return phone_number.isdigit()

def add_client(first_name, last_name, email):
    """
    Добавляет нового клиента в базу данных.

    :param first_name: Имя клиента.
    :param last_name: Фамилия клиента.
    :param email: Электронная почта клиента.
    :return: ID добавленного клиента.
    """
    if not validate_email(email):
        print("Некорректный формат электронной почты.")
        return

    query = '''
        INSERT INTO client (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id;
    '''
    result = execute_query(query, (first_name, last_name, email))
    if result:
        return result[0][0]

def add_phone(client_id, phone_number):
    """
    Добавляет новый номер телефона для клиента в базу данных.

    :param client_id: ID клиента.
    :param phone_number: Номер телефона клиента.
    """
    if not validate_phone(phone_number):
        print("Номер телефона должен содержать только цифры.")
        return

    query = '''
        INSERT INTO phone (client_id, phone_number) VALUES (%s, %s);
    '''
    execute_query(query, (client_id, phone_number))

def update_client(client_id, first_name=None, last_name=None, email=None):
    """
    Обновляет информацию о клиенте в базе данных.

    :param client_id: ID клиента.
    :param first_name: Новое имя клиента.
    :param last_name: Новая фамилия клиента.
    :param email: Новая электронная почта клиента.
    """
    if first_name:
        query = '''
            UPDATE client SET first_name=%s WHERE id=%s;
        '''
        execute_query(query, (first_name, client_id))
    if last_name:
        query = '''
            UPDATE client SET last_name=%s WHERE id=%s;
        '''
        execute_query(query, (last_name, client_id))
    if email:
        query = '''
            UPDATE client SET email=%s WHERE id=%s;
        '''
        execute_query(query, (email, client_id))


def delete_phone(client_id, phone_number):
    """
    Удаляет номер телефона клиента из базы данных.

    :param client_id: ID клиента.
    :param phone_number: Номер телефона для удаления.
    """
    query = '''
        DELETE FROM phone WHERE client_id=%s AND phone_number=%s;
    '''
    execute_query(query, (client_id, phone_number))


def delete_client(client_id):
    """
    Удаляет клиента и его номера телефонов из базы данных.

    :param client_id: ID клиента.
    """
    query_phone = '''
        DELETE FROM phone WHERE client_id=%s;
    '''
    execute_query(query_phone, (client_id,))
    query_client = '''
        DELETE FROM client WHERE id=%s;
    '''
    execute_query(query_client, (client_id,))


def find_client(first_name=None, last_name=None, email=None, phone_number=None):
    """
    Ищет клиента в базе данных по указанным параметрам.

    :param first_name: Имя клиента.
    :param last_name: Фамилия клиента.
    :param email: Электронная почта клиента.
    :param phone_number: Номер телефона клиента.
    :return: Результат поиска (список клиентов).
    """
    query = '''
        SELECT client.id, first_name, last_name, email, phone_number FROM client
        LEFT JOIN phone ON client.id = phone.client_id WHERE
    '''
    params = []
    conditions = []
    if first_name:
        conditions.append("first_name=%s")
        params.append(first_name)
    if last_name:
        conditions.append("last_name=%s")
        params.append(last_name)
    if email:
        conditions.append("email=%s")
        params.append(email)
    if phone_number:
        conditions.append("phone_number=%s")
        params.append(phone_number)

    query += " AND ".join(conditions)
    return execute_query(query, tuple(params))


def check_data():
    """
    Проверяет и выводит данные клиентов и номеров телефонов из базы данных.
    """
    query_clients = 'SELECT * FROM client;'
    clients = execute_query(query_clients)
    print("Clients:", clients)

    query_phones = 'SELECT * FROM phone;'
    phones = execute_query(query_phones)
    print("Phones:", phones)


if __name__ == "__main__":
    client_id = add_client("Андрей", "Овчинников", "andrey@mail.ru")
    add_phone(client_id, "75555555555")
    add_phone(client_id, "85555555555")
    check_data()

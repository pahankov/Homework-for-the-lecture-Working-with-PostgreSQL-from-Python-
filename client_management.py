import psycopg2
from config import DATABASE
from validation import validate_email, validate_phone
from db_utils import get_connection, execute_query

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
        return None

    query = '''
        INSERT INTO client (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id;
    '''
    result = execute_query(query, (first_name, last_name, email))
    if result:
        return result[0]
    else:
        print("Не удалось добавить клиента.")
        return None


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
    result = execute_query(query, (client_id, phone_number))
    if result is None:
        print(f"Не удалось добавить номер телефона {phone_number} для клиента с ID {client_id}.")
    else:
        print(f"Номер телефона {phone_number} успешно добавлен для клиента с ID {client_id}.")



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
        result = execute_query(query, (first_name, client_id))
        if result is None:
            print("Не удалось обновить имя клиента.")

    if last_name:
        query = '''
            UPDATE client SET last_name=%s WHERE id=%s;
        '''
        result = execute_query(query, (last_name, client_id))
        if result is None:
            print("Не удалось обновить фамилию клиента.")

    if email and validate_email(email):
        query = '''
            UPDATE client SET email=%s WHERE id=%s;
        '''
        result = execute_query(query, (email, client_id))
        if result is None:
            print("Не удалось обновить email клиента.")
    elif email:
        print("Некорректный формат электронной почты.")


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

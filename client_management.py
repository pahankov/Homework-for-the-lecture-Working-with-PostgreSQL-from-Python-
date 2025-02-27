import psycopg2
from config import DATABASE

def get_connection():
    return psycopg2.connect(**DATABASE)

def create_db():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO public;')
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS client (
                        id SERIAL PRIMARY KEY,
                        first_name VARCHAR(50),
                        last_name VARCHAR(50),
                        email VARCHAR(100)
                    );
                    CREATE TABLE IF NOT EXISTS phone (
                        id SERIAL PRIMARY KEY,
                        client_id INTEGER REFERENCES client(id),
                        phone_number VARCHAR(20)
                    );
                ''')
                conn.commit()
    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных: {e}")

def add_client(first_name, last_name, email):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO client (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id;
                ''', (first_name, last_name, email))
                client_id = cur.fetchone()[0]
                conn.commit()
                return client_id
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении клиента: {e}")

# Остальные методы остаются без изменений


def add_phone(client_id, phone_number):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO phone (client_id, phone_number) VALUES (%s, %s);
                ''', (client_id, phone_number))
                conn.commit()
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении телефона: {e}")

def update_client(client_id, first_name=None, last_name=None, email=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if first_name:
                    cur.execute('''
                        UPDATE client SET first_name=%s WHERE id=%s;
                    ''', (first_name, client_id))
                if last_name:
                    cur.execute('''
                        UPDATE client SET last_name=%s WHERE id=%s;
                    ''', (last_name, client_id))
                if email:
                    cur.execute('''
                        UPDATE client SET email=%s WHERE id=%s;
                    ''', (email, client_id))
                conn.commit()
    except psycopg2.Error as e:
        print(f"Ошибка при обновлении клиента: {e}")

def delete_phone(client_id, phone_number):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    DELETE FROM phone WHERE client_id=%s AND phone_number=%s;
                ''', (client_id, phone_number))
                conn.commit()
    except psycopg2.Error as e:
        print(f"Ошибка при удалении телефона: {e}")


def delete_client(client_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    DELETE FROM phone WHERE client_id=%s;
                ''', (client_id,))
                cur.execute('''
                    DELETE FROM client WHERE id=%s;
                ''', (client_id,))
                conn.commit()
    except psycopg2.Error as e:
        print(f"Ошибка при удалении клиента: {e}")


def find_client(first_name=None, last_name=None, email=None, phone_number=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
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
                cur.execute(query, tuple(params))
                result = cur.fetchall()
                return result
    except psycopg2.Error as e:
        print(f"Ошибка при поиске клиента: {e}")


def check_data():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM client;')
                clients = cur.fetchall()
                print("Clients:", clients)

                cur.execute('SELECT * FROM phone;')
                phones = cur.fetchall()
                print("Phones:", phones)
    except psycopg2.Error as e:
        print(f"Ошибка при проверке данных: {e}")


if __name__ == "__main__":
    create_db()
    client_id = add_client("John", "Doe", "johndoe@example.com")
    add_phone(client_id, "123-456-7890")
    add_phone(client_id, "098-765-4321")
    check_data()

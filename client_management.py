import psycopg2


def create_db():
    conn = psycopg2.connect(database="client_management", user="pahankov", password="Circul77", host="localhost",
                            port="5432")
    cur = conn.cursor()
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
    conn.close()


def add_client(first_name, last_name, email):
    conn = psycopg2.connect(database="client_management", user="pahankov", password="Circul77", host="localhost",
                            port="5432")
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO client (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id;
    ''', (first_name, last_name, email))
    client_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return client_id


def add_phone(client_id, phone_number):
    conn = psycopg2.connect(database="client_management", user="pahankov", password="Circul77", host="localhost",
                            port="5432")
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO phone (client_id, phone_number) VALUES (%s, %s);
    ''', (client_id, phone_number))
    conn.commit()
    conn.close()


def update_client(client_id, first_name=None, last_name=None, email=None):
    conn = psycopg2.connect(database="client_management", user="pahankov", password="Circul77", host="localhost",
                            port="5432")
    cur = conn.cursor()
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
    conn.close()


def delete_phone(client_id, phone_number):
    conn = psycopg2.connect(database="client_management", user="pahankov", password="Circul77", host="localhost",
                            port="5432")
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM phone WHERE client_id=%s AND phone_number=%s;
    ''', (client_id, phone_number))
    conn.commit()
    conn.close()


def delete_client(client_id):
    conn = psycopg2.connect(database="client_management", user="pahankov", password="Circul77", host="localhost",
                            port="5432")
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM phone WHERE client_id=%s;
    ''', (client_id,))
    cur.execute('''
        DELETE FROM client WHERE id=%s;
    ''', (client_id,))
    conn.commit()
    conn.close()


def find_client(first_name=None, last_name=None, email=None, phone_number=None):
    conn = psycopg2.connect(database="client_management", user="pahankov", password="Circul77", host="localhost",
                            port="5432")
    cur = conn.cursor()
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
    conn.close()
    return result


def check_data():
    conn = psycopg2.connect(database="client_management", user="pahankov", password="Circul77", host="localhost",
                            port="5432")
    cur = conn.cursor()

    cur.execute('SELECT * FROM client;')
    clients = cur.fetchall()
    print("Clients:", clients)

    cur.execute('SELECT * FROM phone;')
    phones = cur.fetchall()
    print("Phones:", phones)

    conn.close()


if __name__ == "__main__":
    create_db()
    client_id = add_client("John", "Doe", "johndoe@example.com")
    add_phone(client_id, "123-456-7890")
    add_phone(client_id, "098-765-4321")
    check_data()

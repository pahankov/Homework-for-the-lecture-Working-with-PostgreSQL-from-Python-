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

if __name__ == "__main__":
    create_db()

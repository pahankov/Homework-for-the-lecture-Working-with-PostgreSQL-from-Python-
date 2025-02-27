import psycopg2
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

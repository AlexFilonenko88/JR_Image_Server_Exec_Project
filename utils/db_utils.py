import logging
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def get_connection():
    """Создаёт и возвращает соединение с базой данных"""

    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )


def test_connection():
    """Тест подключения к базе данных"""

    conn = None
    try:
        conn = get_connection()
        logger.info("Соединение с базой данных успешно установленно")
    except Exception as e:
        logger.info(f"Ошибка подключения: {e}")
    finally:
        if conn:
            logger.info("Соединение с базой данных закрыто")
            conn.close()


def create_table():
    """Создание таблицы images_server"""

    query = """
        CREATE TABLE IF NOT EXISTS images_server (
            id SERIAL PRIMARY KEY,
            filename TEXT NOT NULL,
            original_name TEXT NOT NULL,
            size INTEGER NOT NULL,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            file_type TEXT NOT NULL
        );
    """

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()
        logger.info("Таблица images_server создана (или уже существует)")
    except Exception as e:
        logger.info(f"Ошибка создания таблицы: {e}")
    finally:
        if conn:
            logger.info("После создания таблицы соединение с базой данных закрыто")
            conn.close()


def insert_data(filename: str, original_name: str, size: int, file_type: str):
    """Добавление данных в таблицу images_server"""

    query = """
        INSERT INTO images_server (
            filename,
            original_name,
            size,
            file_type
        )
        VALUES (%s, %s, %s, %s);
    """

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (filename, original_name, size, file_type))
        conn.commit()
        cur.close()
        logger.info("Данные добавлены в таблицу images_server")
    except Exception as e:
        logger.info(f"Ошибка добавления данных в таблицу images_server: {e}")
    finally:
        if conn:
            logger.info("После добавления данных соединение с базой данных закрыто")
            conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_connection()
    create_table()

import logging
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def test_connection():
    """Тест подключения к базе данных"""

    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
        )
        logger.info("Соединение с базой данных успешно")
    except Exception as e:
        logger.info(f"Ошибка подключения: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_connection()

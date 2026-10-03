import asyncio
import logging
import os
from typing import Any

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()

logger = logging.getLogger(__name__)

PAGE_SIZE = 10


async def get_connection_db() -> psycopg.AsyncConnection:
    """Создаёт и возвращает соединение с базой данных"""

    return await psycopg.AsyncConnection.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )


async def test_connection_db() -> None:
    """Тест подключения к базе данных"""

    conn = None
    try:
        conn = await get_connection_db()
        logger.info("Соединение с базой данных успешно установленно")
    except Exception as e:
        logger.info(f"Ошибка подключения: {e}")
    finally:
        if conn:
            logger.info("Соединение с базой данных закрыто")
            await conn.close()


async def create_table_db() -> None:
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
        conn = await get_connection_db()
        async with conn.cursor() as cur:
            await cur.execute(query)
        await conn.commit()
        logger.info("Таблица images_server создана (или уже существует)")
    except Exception as e:
        logger.info(f"Ошибка создания таблицы images_server: {e}")
    finally:
        if conn:
            logger.info(
                "После создания таблицы images_server, соединение с базой данных закрыто"
            )
            await conn.close()


async def insert_image_db(
    filename: str, original_name: str, size: int, file_type: str
) -> None:
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
        conn = await get_connection_db()
        async with conn.cursor() as cur:
            await cur.execute(query, (filename, original_name, size, file_type))
        await conn.commit()
        logger.info("Данные добавлены в таблицу images_server")
    except Exception as e:
        logger.info(f"Ошибка добавления данных в таблицу images_server: {e}")
    finally:
        if conn:
            logger.info(
                "После добавления данных в таблицу images_server, соединение с базой данных закрыто"
            )
            await conn.close()


async def delete_image_db(filename: str) -> None:
    """Удаление данных из таблицы images_server"""

    query = """
        DELETE FROM images_server
        WHERE filename = %s;
    """

    conn = None
    try:
        conn = await get_connection_db()
        async with conn.cursor() as cur:
            await cur.execute(query, (filename,))
        await conn.commit()
        logger.info("Данные удалены из таблицы images_server")
    except Exception as e:
        logger.info(f"Ошибка удаления данных из таблицы images_server: {e}")
    finally:
        if conn:
            logger.info(
                "После удаления данных из таблицы images_server, соединение с базой данных закрыто"
            )
            await conn.close()


async def get_images_page_db(limit: int, offset: int) -> list[dict[str, Any]]:
    """Получение страницы изображений: LIMIT/OFFSET, свежие записи сверху"""

    query = """
        SELECT * FROM images_server
        ORDER BY upload_time DESC
        LIMIT %s OFFSET %s;
    """

    conn = None
    try:
        conn = await get_connection_db()
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(query, (limit, offset))
            rows = await cur.fetchall()
        logger.info(f"Получена страница изображений: limit={limit}, offset={offset}")
        return [dict(row) for row in rows]
    except Exception as e:
        logger.info(f"Ошибка получения страницы изображений: {e}")
        return []
    finally:
        if conn:
            logger.info("После получения страницы изображений, соединение закрыто")
            await conn.close()


async def count_images_db() -> int:
    """Подсчёт количества изображений для расчёта числа страниц"""

    query = """
        SELECT COUNT(*) FROM images_server;
    """

    conn = None
    try:
        conn = await get_connection_db()
        async with conn.cursor() as cur:
            await cur.execute(query)
            row = await cur.fetchone()
        total = int(row[0]) if row else 0
        logger.info(f"Всего изображений в базе: {total}")
        return total
    except Exception as e:
        logger.info(f"Ошибка подсчёта изображений: {e}")
        return 0
    finally:
        if conn:
            logger.info("После подсчёта изображений, соединение закрыто")
            await conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    async def main() -> None:
        await test_connection_db()
        await create_table_db()

    asyncio.run(main())

from pathlib import Path
import asyncio
import aiofiles


ALLOWED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp", ".gif"]
MAX_UPLOAD_SIZE = 5 * 1024 * 1024


def is_allowed_file(filename: str) -> bool:
    ''' Проверка, являеться файл допуститимым для загрузки '''

    ext = Path(filename).suffix.lower()

    return ext in ALLOWED_EXTENSIONS


def get_unique_name(filename: str) -> str:
    pass


async def save_uploaded_file(file, filename, UPLOAD_DIR):
    file_path = UPLOAD_DIR / filename
    
    async with aiofiles.open(file_path, 'wb') as bf:
        while chunk := await file.read(1024*1024):
            await bf.write(chunk)

if __name__ == '__main__':
    print(is_allowed_file(Path('test.png')))
    print(is_allowed_file(Path('test.mp4')))
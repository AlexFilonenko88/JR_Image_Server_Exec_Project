from pathlib import Path
import aiofiles
import uuid 
import logging


logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp", ".gif"]
MAX_UPLOAD_SIZE = 5 * 1024 * 1024


def is_allowed_expansion_file_name(filename: str) -> bool:
    ''' Проверка, являеться файл допуститимым для загрузки '''

    ext = Path(filename).suffix.lower()
    logger.info(f'Получаем расширение файла: {ext}')

    return ext in ALLOWED_EXTENSIONS


async def check_size_uploaded_image(file):
    ''' Проверка размера загружаемого изображения '''

    content = await file.read(MAX_UPLOAD_SIZE + 1)
    await file.seek(0)

    if len(content) > MAX_UPLOAD_SIZE:
        logger.error(f'Размер файла превышает допустимый размер 5Мб. Ваш размер файла {MAX_UPLOAD_SIZE / 1024 / 1024}Мб')
        
        return False

    return True

def get_list_uploaded_images(UPLOAD_DIR):
    ''' Получить список загруженных изображений '''

    images = [
            file.name
            for file in UPLOAD_DIR.iterdir()
            if file.is_file()
            and file.suffix.lower() in ALLOWED_EXTENSIONS
        ]
    logger.info(f'Получаем список изображений: {images}')
    return images


async def get_unique_name(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    unique_name = f'{uuid.uuid4().hex}{ext}'
    logger.info(f'Получаем униальное имя изображения: {unique_name}')

    return unique_name
    

async def save_uploaded_file(file, filename, UPLOAD_DIR):
    ''' Сохранение загружаемых изображений '''

    file_path = UPLOAD_DIR / filename
    
    async with aiofiles.open(file_path, 'wb') as bf:
        while chunk := await file.read(1024*1024):
            await bf.write(chunk)

    logger.info(f'Сохряняем изображение: {file_path}')


if __name__ == '__main__':
    pass
from pathlib import Path
import os
import asyncio
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import logging
import datetime
from utils.file_utils import (
    is_allowed_expansion_file_name, save_uploaded_file, 
    get_list_uploaded_images, get_unique_name,
    check_size_uploaded_image
)


logs_dir = Path('logs')
logs_dir.mkdir(exist_ok=True)

log_file = logs_dir / 'app.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(),
    ],
    force=True,
)

logger = logging.getLogger(__name__)


app = FastAPI()

UPLOAD_DIR = Path('image_uploader')
UPLOAD_DIR.mkdir(exist_ok=True)

app.mount('/css', StaticFiles(directory='templates/css'), name='css')
app.mount('/js', StaticFiles(directory='templates/js'), name='js')
app.mount('/img', StaticFiles(directory='templates/img'), name='img')
app.mount('/image_uploader', StaticFiles(directory='image_uploader'), name='image_uploader')

templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    ''' Главная страница сервиса. '''

    images = get_list_uploaded_images(UPLOAD_DIR)
    logger.info(f'Получен список изображений: {images}, для "/"')

    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={
            'images': images,
        }
    )


@app.get('/images/', response_class=HTMLResponse)
async def images(request: Request):
    ''' Страница изображений сервиса. '''

    images = get_list_uploaded_images(UPLOAD_DIR)
    logger.info(f'Получен список изображений: {images}, для "images"')

    return templates.TemplateResponse(
        request=request,
        name='images.html',
        context={
            'images': images,
        }
    )


@app.get('/upload', response_class=HTMLResponse)
async def upload(request: Request):
    ''' Страница загрузки изображений. GET '''

    return templates.TemplateResponse(
        request=request,
        name='upload.html',
        context={}
    )


@app.post('/upload/')
async def upload_file(file: UploadFile = File(...)):
    ''' Страница загрузки изображений. POST '''

    # TODO  1. Исправить drag & drop
    # TODO  2. Добавить кнопку удаления изображения с страницы images
    # TODO  5. Docker
    # TODO  6. "Прикрутить nginx", сначало как работает, зачем нужен ?

    if not UPLOAD_DIR.is_dir():
        logger.info(f'Папка "{UPLOAD_DIR}" не существует, создаем')
        UPLOAD_DIR.mkdir(exist_ok=True)

    file_name = file.filename
    logger.info(f'Получаем имя файла: {file_name}')

    if not is_allowed_expansion_file_name(file_name):
        logger.error(f'Недопустимый формат файла: {file_name}')
        raise HTTPException(
            status_code=400,
            detail='Недопустимый формат файла. Разрешены: .png, .jpg, .jpeg, .webp, .gif'
        )

    is_valid_size_uplod_file = await check_size_uploaded_image(file)

    if not is_valid_size_uplod_file:
        raise HTTPException(
                    status_code=400,
                    detail='Размер файла превышает допустимый размер 5Mб'
                )

    new_file_name = await get_unique_name(file_name)
    logger.info(f'Получаем имя нового файла: {new_file_name}')

    await save_uploaded_file(file, new_file_name, UPLOAD_DIR)

    return {
        'url': f'/images/{file.filename}'
    }


if __name__ == '__main__':
    # uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
    uvicorn.run("app:app", host="127.0.0.1", port=8000)

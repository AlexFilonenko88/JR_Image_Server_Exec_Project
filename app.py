from pathlib import Path
import asyncio
import aiofiles
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from utils.file_utils import ALLOWED_EXTENSIONS


app = FastAPI()

app.mount('/css', StaticFiles(directory='templates/css'), name='css')
app.mount('/js', StaticFiles(directory='templates/js'), name='js')
app.mount('/img', StaticFiles(directory='templates/img'), name='img')
app.mount('/image_uploader', StaticFiles(directory='image_uploader'), name='image_uploader')

templates = Jinja2Templates(directory='templates')

UPLOAD_DIR = Path('image_uploader')
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    ''' Главная страница сервиса. '''

    images = [
        file.name
        for file in UPLOAD_DIR.iterdir()
        if file.is_file()
        and file.suffix.lower() in ALLOWED_EXTENSIONS
    ]

    print(images)

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

    return templates.TemplateResponse(
        request=request,
        name='images.html',
        context={}
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

    # TODO  1. Проверка допустимого размера файла
    # TODO  2. Сохранение файла с уникальныи именем
    # TODO  3. Возврат ссылки на файл (f'/images/{file.filename}')
    # TODO  4. Проверка уникальности имени и расширения
    # TODO  5. Реализовать ввиде функции?; выносить каждую функцию в отдельный файл ?
    # TODO  6. Реализовать кнопеку копирование 

    file_path = UPLOAD_DIR / file.filename

    async with aiofiles.open(file_path, 'wb') as bf:
        data = await file.read()
        await bf.write(data)

    return {
        'url': f'/images/{file.filename}'
    }

    # return templates.TemplateResponse(
    #     request=request,
    #     name='upload.html',
    #     context={}
    # )


if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

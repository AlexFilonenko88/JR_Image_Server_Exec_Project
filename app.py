from pathlib import Path
import asyncio
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from utils.file_utils import is_allowed_file, save_uploaded_file, get_list_uploaded_images, ALLOWED_EXTENSIONS


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

    # TODO  1. Проверка допустимого размера файла
    # TODO  2. Сохранение файла с уникальныи именем
    # TODO  3. Возврат ссылки на файл (f'/images/{file.filename}')
    # TODO  4. Проверка уникальности имени и расширения
    # TODO  5. "Прикрутить nginx", сначало как работает, зачем нужен ?
    # TODO  6. Docker

    if not UPLOAD_DIR.is_dir():
        UPLOAD_DIR.mkdir(exist_ok=True)

    file_name = file.filename

    if not is_allowed_file(file_name):
        raise HTTPException(
            status_code=400,
            detail='Недопустимый формат файла. Разрешены: .png, .jpg, .jpeg, .webp, .gif'
        )

    await save_uploaded_file(file, file_name, UPLOAD_DIR)

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

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn


app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    ''' Главная страница сервиса. '''

    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={}
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


@app.post('/upload/', response_class=HTMLResponse)
async def upload(request: Request):
    ''' Страница загрузки изображений. POST '''

    return templates.TemplateResponse(
        request=request,
        name='upload.html',
        context={}
    )


if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

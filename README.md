# Image Upload Service

Веб-сервис на FastAPI для загрузки, хранения и просмотра изображений.

## Возможности

- Загрузка изображений через веб-форму (`/upload`)
- Просмотр списка загруженных изображений (`/images`)
- Валидация формата файла (разрешены: `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`)
- Валидация размера файла (максимум 5 МБ)
- Автоматическая генерация уникального имени файла (UUID) во избежание коллизий
- Логирование операций в файл (`logs/app.log`) и в консоль

## Стек технологий

- **FastAPI** 0.141.1 — веб-фреймворк
- **Uvicorn** 0.52.3 — ASGI-сервер
- **Jinja2** 3.1.6 — шаблонизатор для рендеринга HTML-страниц
- **aiofiles** 25.1.0 — асинхронная работа с файловой системой
- **python-multipart** 0.0.32 — обработка multipart-запросов (загрузка файлов)

## Структура проекта

```
.
├── app.py                  # Точка входа, роуты FastAPI
├── utils/
│   └── file_utils.py       # Валидация, сохранение и получение списка файлов
├── templates/               # Jinja2-шаблоны + статика (css, js, img)
├── images/                  # Директория для загруженных изображений
└── logs/
    └── app.log               # Файл логов
```

## Установка

Создайте файл `requirements.txt` со следующим содержимым:

```
fastapi==0.141.1
uvicorn==0.52.3
Jinja2==3.1.6
aiofiles==25.1.0
python-multipart==0.0.32
```

Затем установите зависимости:

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python app.py
```

Сервис будет доступен по адресу [http://127.0.0.1:8080](http://127.0.0.1:8080).

## Эндпоинты

| Метод | Путь        | Описание                                   |
|-------|-------------|---------------------------------------------|
| GET   | `/`         | Главная страница со списком изображений      |
| GET   | `/images`   | Страница со списком загруженных изображений  |
| GET   | `/upload`   | Страница с формой загрузки                   |
| POST  | `/upload/`  | Загрузка файла (multipart/form-data, поле `file`) |

Пример ответа `POST /upload/`:

```json
{
  "url": "/images/<уникальное_имя_файла>.png"
}
```

## Известные ограничения / TODO

- Не работает drag & drop на странице в Yandex браузере



### Резервное копирование базы данных

Для резервного копирования используется PostgreSQL `pg_dump`, запущенный внутри Docker-контейнера `postgres`.

### Создание резервной копии вручную

Запустить:

```bash
python utils/scripts_backups/backup.py
```
Альтернативная команда:
```bash
python3 -m utils.scripts_backups.backup  
```

Резервная копия сохраняется в директорию:

```text
backups/
```

Имя файла содержит дату и время создания:

```text
backup_2026-10-01_100530.sql
```

Также backup можно создать непосредственно командой:

```bash
docker compose exec -T postgres \
    pg_dump -U postgres images_db \
    > backups/backup_$(date +%Y-%m-%d_%H%M%S).sql
```

### Восстановление базы данных

Для восстановления используется файл резервной копии:

```bash
docker compose exec -T postgres \
    psql -U postgres images_db \
    < backups/backup_2026-10-01_100530.sql
```

Или:

```bash
python utils/scripts_backups/restore.py backups/backup_2026-10-01_100530.sql
```
Альтернативная команда:
```bash
python3 -m utils.scripts_backups.restore backups/backup_2026-10-01_111901.sql 
```

### Автоматическое резервное копирование

Для автоматического создания резервных копий используется `cron`.

Пример запуска backup каждый день в 03:00:

```cron
0 3 * * * cd /home/alex/Projects/Exam_projects/Image_Server_Exec_Project && /usr/bin/python3 scripts/backup.py >> logs/backup.log 2>&1
```

Все созданные резервные копии хранятся в директории:

```text
/backups
```

### Проверка резервных копий

Список созданных резервных копий:

```bash
ls -lh backups/
```

Проверить содержимое SQL-файла:
    print(f"База данных восстановлена из: {path}")
```bash
head -n 20 backups/backup_2026-10-01_100530.sql
```

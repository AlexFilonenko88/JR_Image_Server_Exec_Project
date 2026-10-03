# Image Upload Service

Веб-сервис на FastAPI для загрузки, хранения и просмотра изображений.
Метаданные файлов хранятся в PostgreSQL, список изображений отдаётся
постранично (`LIMIT`/`OFFSET`).

## Возможности

- Загрузка изображений через веб-форму (`/upload`), включая drag & drop
- Просмотр списка загруженных изображений с пагинацией (`/images_list`)
- Постраничная выборка: по 10 записей, сортировка по дате загрузки (свежие сверху)
- Навигация «Предыдущая страница» / «Следующая страница» с отключением кнопок
  на первой и последней страницах
- Публичная ссылка на каждый файл, кнопки «КОПИРОВАТЬ» и «Открыть»
- Удаление изображения (файл с диска + запись в БД)
- Валидация формата файла (разрешены: `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`)
- Валидация размера файла (максимум 5 МБ)
- Автоматическая генерация уникального имени файла (UUID) во избежание коллизий
- Создание таблицы `images_server` при старте приложения
- Логирование операций в файл (`logs/app.log`) и в консоль
- Резервное копирование и восстановление БД через `pg_dump` / `psql`

## Стек технологий

- **Python** 3.14
- **FastAPI** 0.141.1 — веб-фреймворк
- **Uvicorn** 0.52.3 — ASGI-сервер
- **Jinja2** 3.1.6 — шаблоны HTML-страниц
- **psycopg** 3.3.6 — асинхронный драйвер PostgreSQL
- **PostgreSQL** 18 — хранилище метаданных
- **aiofiles** 25.1.0 — асинхронная работа с файловой системой
- **python-multipart** 0.0.32 — обработка `multipart/form-data`
- **python-dotenv** 1.2.3 — чтение настроек из `.env`
- **Docker Compose** — сборка и запуск app + postgres + pgAdmin + nginx
- **nginx** 1.30 — reverse proxy и раздача файлов из `/images/`
- **Ruff**, **mypy**, **pre-commit** — линтинг, типы, проверки перед коммитом

## Структура проекта

```text
.
├── app.py                       # Точка входа, роуты FastAPI
├── Dockerfile                   # Образ приложения
├── docker-compose.yml           # app + postgres + pgadmin + nginx
├── nginx.conf                   # Reverse proxy + раздача статики /images/
├── requirements.txt             # Зависимости для сборки Docker-образа
├── pyproject.toml               # Poetry + настройки ruff/mypy
├── .env                         # Локальные настройки (не в репозитории)
├── utils/
│   ├── db_utils.py              # Подключение к БД, CRUD, LIMIT/OFFSET, PAGE_SIZE
│   ├── file_utils.py            # Валидация, сохранение, удаление файлов, pluralize
│   ├── gap_separator_file_handler.py  # Логгер с разделителем между сессиями
│   └── scripts_backups/
│       ├── backup.py            # pg_dump в backups/
│       └── restore.py           # Восстановление из файла резервной копии
├── templates/                   # Jinja2-шаблоны + статика
│   ├── index.html
│   ├── upload.html
│   ├── images_list.html         # Список изображений + блок пагинации
│   ├── css/                     # reset.css, style.css
│   ├── js/                      # index.js, upload.js
│   └── img/
├── images/                      # Загруженные изображения
├── import/                      # SQL-файлы для импорта в pgAdmin
├── backups/                     # Резервные копии БД
└── logs/
    └── app.log                  # Логи приложения
```

## Требования

- Python >= 3.14
- Docker и Docker Compose (для запуска с БД в контейнере)
- Либо локальный PostgreSQL 18, если приложение запускается без Docker

## Установка

```bash
git clone <URL репозитория>
cd Image_Server_Exec_Project

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
# либо: poetry install
```

## Переменные окружения

Настройки читаются из файла `.env` в корне проекта (через `python-dotenv`).
Создайте `.env` и заполните значения:

```dotenv
# Приложение
APP_HOST=127.0.0.1
APP_PORT=8000
NGINX_PORT=8080

# PostgreSQL
POSTGRES_DB=images_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<ваш_пароль>
POSTGRES_HOST=postgres     # для запуска внутри docker compose; локально: localhost
POSTGRES_PORT=5432

# pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=<пароль_pgadmin>
PGADMIN_PORT=5050
```

> Пароли в репозиторий не коммитятся: `.env` исключён через `.gitignore`.

## Запуск

### Локально (нужен доступный PostgreSQL)

```bash
python app.py
```

Сервис доступен по адресу <http://127.0.0.1:8000>.
Таблица `images_server` создаётся автоматически при старте.

### Через Docker Compose

```bash
docker compose up --build -d
```

| Сервис   | Адрес                          |
| -------- | ------------------------------ |
| app      | `http://${APP_HOST}:${APP_PORT}` |
| nginx    | `http://localhost:${NGINX_PORT}` |
| pgAdmin  | `http://localhost:${PGADMIN_PORT}` |
| postgres | `localhost:${POSTGRES_PORT}`   |

Остановка и удаление контейнеров:

```bash
docker compose down          # с сохранением данных
docker compose down -v       # вместе с томами (данные БД будут удалены)
```

## Эндпоинты

| Метод | Путь                 | Описание                                                   |
| ----- | -------------------- | ---------------------------------------------------------- |
| GET   | `/`                  | Главная страница                                           |
| GET   | `/upload`            | Форма загрузки изображения                                 |
| POST  | `/upload/`           | Загрузка файла (`multipart/form-data`, поле `file`)        |
| GET   | `/images_list`       | Список изображений с пагинацией (`?page=N`, по 10 записей) |
| POST  | `/delete/{filename}` | Удаление изображения (файл + запись в БД)                  |
| GET   | `/images/{filename}` | Отдача файла (через nginx в Docker или `StaticFiles` локально) |

### Загрузка

```bash
curl -F "file=@photo.png" http://127.0.0.1:8000/upload/
```

Ответ:

```json
{
  "url": "/images/<уникальное_имя_файла>.png"
}
```

### Удаление

```bash
curl -X POST http://127.0.0.1:8000/delete/<уникальное_имя_файла>.png
```

Ответ:

```json
{
  "status": "ok",
  "filename": "<уникальное_имя_файла>.png"
}
```

Ответ `404`, если файл на диске не найден.

## Пагинация списка изображений

Страница `/images_list` принимает параметр `page` (по умолчанию 1,
минимум 1, значения за пределами диапазона обрезаются до последней
существующей страницы).

Размер страницы задаётся константой `PAGE_SIZE` в `utils/db_utils.py`
(по умолчанию 10).

Выборка выполняется запросами (таблица `images_server`):

```sql
SELECT * FROM images_server
ORDER BY upload_time DESC
LIMIT 10 OFFSET <смещение>;

SELECT COUNT(*) FROM images_server;
```

где `смещение = (page - 1) * PAGE_SIZE`.

Поведение навигации:

- на первой странице кнопка «Предыдущая страница» отключена;
- на последней странице кнопка «Следующая страница» отключена;
- между кнопками выводится номер текущей страницы, общее число страниц
  и количество записей со склонением («всего 12 элементов»);
- при удалении последней записи на странице (кроме первой) браузер
  автоматически переходит на предыдущую страницу;
- при пустой базе показывается сообщение «Изображений пока нет»,
  навигация остаётся неактивной.

## Схема базы данных

```sql
CREATE TABLE IF NOT EXISTS images_server (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,          -- имя файла на диске (UUID)
    original_name TEXT NOT NULL,     -- исходное имя загруженного файла
    size INTEGER NOT NULL,           -- размер в байтах
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_type TEXT NOT NULL          -- расширение файла
);
```

## Проверка качества кода

```bash
ruff check .            # линтер
ruff format --check .   # форматирование
mypy                    # проверка типов (настройки в pyproject.toml)
pre-commit run --all-files
```

Конфигурации: `.ruff.toml` (`line-length = 88`, правила `E`, `F`, `I`),
раздел `[tool.mypy]` в `pyproject.toml`, `.pre-commit-config.yaml`.

## Резервное копирование базы данных

Резервные копии создаются утилитой `pg_dump` внутри контейнера `postgres`
и сохраняются в директорию `backups/`.

### Создание копии

```bash
python utils/scripts_backups/backup.py
# либо: python3 -m utils.scripts_backups.backup
```

Альтернативная команда напрямую:

```bash
docker compose exec -T postgres \
    pg_dump -U postgres images_db \
    > backups/backup_$(date +%Y-%m-%d_%H%M%S).sql
```

Имя файла содержит дату и время создания:

```text
backup_2026-10-01_100530.sql
```

### Восстановление

```bash
python utils/scripts_backups/restore.py backups/backup_2026-10-01_100530.sql
# либо: python3 -m utils.scripts_backups.restore backups/backup_2026-10-01_100530.sql
```

Альтернативная команда напрямую:

```bash
docker compose exec -T postgres \
    psql -U postgres images_db \
    < backups/backup_2026-10-01_100530.sql
```

### Автоматическое резервное копирование

Через cron (пример — ежедневно в 03:00):

```cron
0 3 * * * cd /home/alex/Projects/Exam_projects/Image_Server_Exec_Project && /usr/bin/python3 utils/scripts_backups/backup.py >> logs/backup.log 2>&1
```

### Проверка резервных копий

```bash
ls -lh backups/
head -n 20 backups/backup_2026-10-01_100530.sql
```

## Известные ограничения / TODO

- Не работает drag & drop на странице загрузки в браузере Яндекс
- Файл и запись в БД удаляются в двух операциях: при сбое между ними
  возможна рассинхронизация диска и базы

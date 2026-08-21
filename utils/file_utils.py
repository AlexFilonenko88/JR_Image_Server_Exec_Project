from pathlib import Path


ALLOWED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp", ".gif"]
MAX_UPLOAD_SIZE = 5 * 1024 * 1024


def is_allowed_file(filename: str) -> bool:
    ''' Проверка, являеться файл допуститимым для загрузки '''

    ext = Path(filename).suffix.lower()

    if ext in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


def get_unique_name(filename: str) -> str:
    pass


if __name__ == '__main__':
    print(is_allowed_file(Path('test.png')))
    print(is_allowed_file(Path('test.mp4')))
import logging
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

from utils.gap_separator_file_handler import GapSeparatorFileHandler

load_dotenv()

logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)
log_file = logs_dir / "backup.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # logging.FileHandler(log_file, encoding="utf-8"),
        GapSeparatorFileHandler(log_file, encoding="utf-8", gap_seconds=300),
        logging.StreamHandler(),
    ],
    force=True,
)

logger = logging.getLogger(__name__)


def restore_backup(backup_file: str) -> None:
    path = Path(backup_file)

    if not path.exists():
        logger.info(f"Файл бэкапа не найден: {path}")
        print(f"Файл бэкапа не найден: {path}")
        sys.exit(1)

    postgres_user = os.getenv("POSTGRES_USER")
    postgres_db = os.getenv("POSTGRES_DB")

    command = [
        "docker",
        "compose",
        "exec",
        "-T",
        "postgres",
        "psql",
        "-U",
        postgres_user,
        postgres_db,
    ]

    with path.open("r", encoding="utf-8") as file:
        subprocess.run(
            command,
            stdin=file,
            check=True,
        )

    logger.info(f"База данных восстановлена из: {path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python scripts/restore.py <backup_file>")
        sys.exit(1)

    restore_backup(sys.argv[1])

import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from utils.gap_separator_file_handler import GapSeparatorFileHandler

load_dotenv()

BACKUP_DIR = Path("backups")

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


def create_backup() -> None:
    BACKUP_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    backup_file = BACKUP_DIR / f"backup_{timestamp}.sql"

    postgres_user = os.getenv("POSTGRES_USER")
    postgres_db = os.getenv("POSTGRES_DB")

    command = [
        "docker",
        "compose",
        "exec",
        "-T",
        "postgres",
        "pg_dump",
        "-U",
        postgres_user,
        postgres_db,
    ]

    with backup_file.open("w", encoding="utf-8") as file:
        subprocess.run(
            command,
            stdout=file,
            check=True,
        )

    logger.info(f"Бэкап создан: {backup_file}")


if __name__ == "__main__":
    create_backup()

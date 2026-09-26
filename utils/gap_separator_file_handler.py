import logging
import os
import time
from datetime import datetime


class GapSeparatorFileHandler(logging.FileHandler):
    """
    FileHandler, добавляет пустую строку-разделитель,
    если между записями прошло больше gap_seconds.

    Добавляет пустую строку перед записью, если:

    - между логами прошло больше gap_seconds;
    - или изменилась дата.

    При запуске приложения время последней записи
    восстанавливается из существующего log-файла.
    """

    def __init__(self, *args, gap_seconds: int = 300, **kwargs):
        super().__init__(*args, **kwargs)

        self.gap_seconds = gap_seconds
        self._last_emit_time: float | None = self._get_last_log_time()

    def _get_last_log_time(self) -> float | None:
        """Возвращает timestamp последней записи в log-файле.

        Читается только небольшой хвост файла,
        а не весь файл.
        """

        try:
            if not os.path.exists(self.baseFilename):
                return None

            with open(self.baseFilename, "rb") as file:
                file.seek(0, os.SEEK_END)

                file_size = file.tell()

                if file_size == 0:
                    return None

                read_size = min(file_size, 4096)

                file.seek(-read_size, os.SEEK_END)

                data: bytes = file.read(read_size)

            lines: list[bytes] = data.splitlines()

            for line_bytes in reversed(lines):
                if not line_bytes.strip():
                    continue

                line = line_bytes.decode(
                    self.encoding or "utf-8",
                    errors="replace",
                )

                timestamp = line[:23]

                dt = datetime.strptime(
                    timestamp,
                    "%Y-%m-%d %H:%M:%S,%f",
                )

                return dt.timestamp()

        except OSError, ValueError:
            return None

        return None

    def emit(self, record: logging.LogRecord) -> None:
        now = record.created

        add_separator = False

        if self._last_emit_time is not None:
            last_dt = datetime.fromtimestamp(self._last_emit_time)
            current_dt = datetime.fromtimestamp(now)

            if now - self._last_emit_time > self.gap_seconds:
                add_separator = True

            if last_dt.date() != current_dt.date():
                add_separator = True

        if add_separator and self.stream is not None:
            try:
                self.stream.write("\n")
                self.flush()
            except Exception:
                self.handleError(record)

        self._last_emit_time = now

        super().emit(record)

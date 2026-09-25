import logging
import time


class GapSeparatorFileHandler(logging.FileHandler):
    """FileHandler, добавляющий пустую строку-разделитель,
    если между записями прошло больше gap_seconds."""

    def __init__(self, *args, gap_seconds: int = 300, **kwargs):
        super().__init__(*args, **kwargs)
        self.gap_seconds = gap_seconds
        self._last_emit_time: float | None = None

    def emit(self, record: logging.LogRecord) -> None:
        now = time.time()

        if (
            self._last_emit_time is not None
            and (now - self._last_emit_time) > self.gap_seconds
        ):
            if self.stream is not None:
                try:
                    self.stream.write("\n")
                    self.flush()
                except Exception:
                    self.handleError(record)

        self._last_emit_time = now
        super().emit(record)

"""Registro JSONL de cada llamada al gateway (insumo del experimento y de la auditoría)."""

import json
import logging
import threading
from datetime import UTC, datetime
from pathlib import Path

log = logging.getLogger("gateway.audit")


class Audit:
    def __init__(self, path: Path | None):
        self._path = path
        self._lock = threading.Lock()

    def record(
        self,
        role: str,
        tool: str,
        path: str | None,
        allowed: bool,
        chars_returned: int = 0,
        bytes_written: int = 0,
        detail: str | None = None,
    ) -> None:
        entry = {
            "ts": datetime.now(UTC).isoformat(timespec="seconds"),
            "role": role,
            "tool": tool,
            "path": path,
            "allowed": allowed,
            "chars_returned": chars_returned,
            "bytes_written": bytes_written,
        }
        if detail:
            entry["detail"] = detail
        log.info("%s", entry)
        if self._path is None:
            return
        try:
            with self._lock:
                self._path.parent.mkdir(parents=True, exist_ok=True)
                with self._path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except OSError as exc:
            log.warning("No se pudo escribir la auditoría: %s", exc)

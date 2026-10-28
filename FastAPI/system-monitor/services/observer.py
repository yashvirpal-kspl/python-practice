import logging
import os
import threading
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from config import settings
from db import connect
from services import alert_service

log = logging.getLogger("observer")

EMAIL_MIN_GAP = 60  # seconds between file-change emails


class FolderHandler(FileSystemEventHandler):
    def __init__(self):
        self._last_email = 0.0
        self._lock = threading.Lock()

    def on_any_event(self, event):
        # Directory "modified" events are noise (fired whenever a child changes)
        if event.event_type in ("opened", "closed", "closed_no_write"):
            return
        if event.is_directory and event.event_type == "modified":
            return
        path = os.fspath(event.src_path)
        if event.event_type == "moved":
            path = f"{path} -> {os.fspath(event.dest_path)}"
        with connect() as c:
            c.execute(
                "INSERT INTO file_events (ts, event, path, is_dir) VALUES (?,?,?,?)",
                (time.time(), event.event_type, path, int(event.is_directory)),
            )
        if settings.watch_email:
            self._maybe_email(event.event_type, path)

    def _maybe_email(self, kind: str, path: str):
        with self._lock:
            now = time.time()
            if now - self._last_email < EMAIL_MIN_GAP:
                return
            self._last_email = now
        threading.Thread(
            target=alert_service.send_email,
            args=(f"[FILE] {kind} on {settings.node_name}", f"{kind}: {path}"),
            daemon=True,
        ).start()


_observer: Observer | None = None


def start():
    global _observer
    paths = [p for p in settings.watch_list if os.path.isdir(p)]
    for p in set(settings.watch_list) - set(paths):
        log.warning("Watch path is not a directory, skipping: %s", p)
    if not paths:
        return
    _observer = Observer()
    handler = FolderHandler()
    for p in paths:
        _observer.schedule(handler, p, recursive=True)
    _observer.start()
    log.info("Watching: %s", paths)


def stop():
    if _observer:
        _observer.stop()
        _observer.join(timeout=5)


def list_events(limit: int) -> list[dict]:
    with connect() as c:
        rows = c.execute("SELECT * FROM file_events ORDER BY ts DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

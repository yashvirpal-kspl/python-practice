import sqlite3
from contextlib import contextmanager

from config import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS samples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL DEFAULT 0,
    node TEXT NOT NULL,
    ts REAL NOT NULL,
    cpu REAL, mem REAL, disk REAL, load1 REAL,
    net_sent_mb REAL, net_recv_mb REAL
);
CREATE INDEX IF NOT EXISTS idx_samples_user_node_ts ON samples(user_id, node, ts);

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL DEFAULT 0,
    node TEXT NOT NULL,
    ts REAL NOT NULL,
    level TEXT NOT NULL,
    message TEXT NOT NULL,
    emailed INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS file_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL NOT NULL,
    event TEXT NOT NULL,
    path TEXT NOT NULL,
    is_dir INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS servers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL DEFAULT 0,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    api_key TEXT NOT NULL DEFAULT '',
    enabled INTEGER NOT NULL DEFAULT 1,
    UNIQUE(user_id, name)
);

-- single admin account (id is always 1), synced from ADMIN_EMAIL / ADMIN_PASSWORD at startup
CREATE TABLE IF NOT EXISTS admin_account (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL
);

-- admin login sessions; only a hash of the token is stored
CREATE TABLE IF NOT EXISTS sessions (
    token_hash TEXT PRIMARY KEY,
    created REAL NOT NULL,
    expires REAL NOT NULL
);

-- user_id 0 is the admin / the host itself and has no row here
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    key_hash TEXT UNIQUE,
    verify_hash TEXT,
    verify_expires REAL,
    verify_sent REAL,
    created REAL NOT NULL
);
"""


@contextmanager
def connect():
    c = sqlite3.connect(settings.db_path, timeout=10)
    c.row_factory = sqlite3.Row
    try:
        yield c
        c.commit()
    finally:
        c.close()


def init_db():
    with connect() as c:
        c.executescript(SCHEMA)

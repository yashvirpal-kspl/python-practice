import time

from config import settings
from db import connect


def record_sample(node: str, snap: dict, user_id: int = 0):
    load = snap["cpu"]["load_avg"]
    disk = max((d["usage_percent"] for d in snap["disks"]), default=0)
    with connect() as c:
        c.execute(
            "INSERT INTO samples (user_id, node, ts, cpu, mem, disk, load1, net_sent_mb, net_recv_mb)"
            " VALUES (?,?,?,?,?,?,?,?,?)",
            (
                user_id,
                node,
                time.time(),
                snap["cpu"]["usage_percent"],
                snap["memory"]["usage_percent"],
                disk,
                load[0] if load else None,
                snap["network"]["bytes_sent_mb"],
                snap["network"]["bytes_recv_mb"],
            ),
        )


def get_history(user_id: int, node: str, minutes: int, limit: int) -> list[dict]:
    since = time.time() - minutes * 60
    with connect() as c:
        # newest `limit` rows in the window, returned oldest-first for charting
        rows = c.execute(
            "SELECT * FROM (SELECT * FROM samples WHERE user_id=? AND node=? AND ts>=?"
            " ORDER BY ts DESC LIMIT ?) ORDER BY ts",
            (user_id, node, since, limit),
        ).fetchall()
    return [dict(r) for r in rows]


def get_nodes(user_id: int) -> list[str]:
    with connect() as c:
        rows = c.execute("SELECT DISTINCT node FROM samples WHERE user_id=? ORDER BY node", (user_id,))
        return [r["node"] for r in rows]


def prune():
    cutoff = time.time() - settings.retention_days * 86400
    with connect() as c:
        c.execute("DELETE FROM samples WHERE ts<?", (cutoff,))
        c.execute("DELETE FROM alerts WHERE ts<?", (cutoff,))
        c.execute("DELETE FROM file_events WHERE ts<?", (cutoff,))

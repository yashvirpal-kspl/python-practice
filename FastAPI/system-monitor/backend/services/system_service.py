import os
import platform
import socket
import time
from datetime import datetime

import psutil

from config import settings

GIB = 1024 ** 3
MIB = 1024 ** 2

# Usage percentages that trigger alerts: (warning, critical)
THRESHOLDS = {
    "cpu": (settings.cpu_warn, settings.cpu_crit),
    "memory": (settings.mem_warn, settings.mem_crit),
    "disk": (settings.disk_warn, settings.disk_crit),
}


def get_host_info():
    boot = psutil.boot_time()
    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "platform": platform.platform(),
        "boot_time": datetime.fromtimestamp(boot).isoformat(),
        "uptime_seconds": int(time.time() - boot),
    }


def get_cpu_info():
    freq = psutil.cpu_freq()
    # getloadavg is emulated on Windows; available natively on Linux VPS
    load = [round(x, 2) for x in os.getloadavg()] if hasattr(os, "getloadavg") else [round(x, 2) for x in psutil.getloadavg()]
    per_core = psutil.cpu_percent(interval=1, percpu=True)
    return {
        "logical_cpus": psutil.cpu_count(),
        "physical_cores": psutil.cpu_count(logical=False),
        "usage_percent": round(sum(per_core) / len(per_core), 1),
        "per_core_percent": per_core,
        "load_avg": load,
        "freq_mhz": round(freq.current, 1) if freq else None,
    }


def get_memory_info():
    vm = psutil.virtual_memory()
    sw = psutil.swap_memory()
    return {
        "total_gib": round(vm.total / GIB, 2),
        "available_gib": round(vm.available / GIB, 2),
        "used_gib": round(vm.used / GIB, 2),
        "usage_percent": vm.percent,
        "swap_total_gib": round(sw.total / GIB, 2),
        "swap_used_gib": round(sw.used / GIB, 2),
        "swap_percent": sw.percent,
    }


def _disk_targets():
    """(label, path, device, fstype) for each disk to report."""
    if settings.disk_list:
        return [(label, path, path, "") for label, path in settings.disk_list]
    return [(p.mountpoint, p.mountpoint, p.device, p.fstype)
            for p in psutil.disk_partitions(all=False)]


def get_disk_info():
    disks = []
    for label, path, device, fstype in _disk_targets():
        try:
            usage = psutil.disk_usage(path)
        except (PermissionError, OSError):
            continue
        disks.append({
            "mountpoint": label,
            "device": device,
            "fstype": fstype,
            "total_gib": round(usage.total / GIB, 2),
            "used_gib": round(usage.used / GIB, 2),
            "free_gib": round(usage.free / GIB, 2),
            "usage_percent": usage.percent,
        })
    return disks


def get_network_info():
    net = psutil.net_io_counters()
    try:
        connections = len(psutil.net_connections())
    except (psutil.AccessDenied, PermissionError):
        connections = None  # needs root on Linux
    return {
        "bytes_sent_mb": round(net.bytes_sent / MIB, 2),
        "bytes_recv_mb": round(net.bytes_recv / MIB, 2),
        "packets_sent": net.packets_sent,
        "packets_recv": net.packets_recv,
        "errors_in": net.errin,
        "errors_out": net.errout,
        "connections": connections,
    }


def get_top_processes(limit: int = 10, sort_by: str = "cpu_percent"):
    attrs = ["pid", "name", "username", "cpu_percent", "memory_percent"]
    procs = list(psutil.process_iter(attrs))
    # First cpu_percent call returns 0.0; prime then sample once
    time.sleep(0.5)
    rows = []
    for p in procs:
        try:
            info = p.as_dict(attrs)
            rows.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    rows.sort(key=lambda r: r.get(sort_by) or 0, reverse=True)
    for r in rows:
        for k in ("cpu_percent", "memory_percent"):
            if r.get(k) is not None:
                r[k] = round(r[k], 1)
    return rows[:limit]


def get_system_info():
    """Full snapshot of the host."""
    return {
        "host": get_host_info(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disks": get_disk_info(),
        "network": get_network_info(),
    }


def evaluate(snapshot: dict) -> list[dict]:
    """Compare a snapshot (local or remote) against thresholds.

    Returns a list of {key, level, message}; level is "warning" or "critical".
    """
    found = []

    def check(key, value, label):
        warn, crit = THRESHOLDS[key.split(":")[0]]
        if value >= crit:
            level = "critical"
        elif value >= warn:
            level = "warning"
        else:
            return
        found.append({"key": key, "level": level, "message": f"{label} at {value}%"})

    check("cpu", snapshot["cpu"]["usage_percent"], "CPU")
    check("memory", snapshot["memory"]["usage_percent"], "Memory")
    for d in snapshot["disks"]:
        check(f"disk:{d['mountpoint']}", d["usage_percent"], f"Disk {d['mountpoint']}")
    return found


def get_health():
    alerts = evaluate(get_system_info())
    status = "ok"
    if any(a["level"] == "critical" for a in alerts):
        status = "critical"
    elif alerts:
        status = "warning"
    return {
        "status": status,
        "alerts": [f"{a['level'].upper()}: {a['message']}" for a in alerts],
    }

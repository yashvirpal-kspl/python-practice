from typing import Literal

from fastapi import APIRouter, Depends, Query

from models.monitor import (
    CpuInfo,
    DiskInfo,
    HealthStatus,
    HostInfo,
    MemoryInfo,
    NetworkInfo,
    ProcessInfo,
    SystemSnapshot,
)
from security import require_admin
from services import system_service

router = APIRouter(
    prefix="/system",
    tags=["system"],
    dependencies=[Depends(require_admin)],
)


@router.get("", response_model=SystemSnapshot)
def system_info():
    return system_service.get_system_info()


@router.get("/health", response_model=HealthStatus)
def health():
    return system_service.get_health()


@router.get("/host", response_model=HostInfo)
def host():
    return system_service.get_host_info()


@router.get("/cpu", response_model=CpuInfo)
def cpu():
    return system_service.get_cpu_info()


@router.get("/memory", response_model=MemoryInfo)
def memory():
    return system_service.get_memory_info()


@router.get("/disks", response_model=list[DiskInfo])
def disks():
    return system_service.get_disk_info()


@router.get("/network", response_model=NetworkInfo)
def network():
    return system_service.get_network_info()


@router.get("/processes", response_model=list[ProcessInfo])
def processes(
    limit: int = Query(10, ge=1, le=100),
    sort_by: Literal["cpu_percent", "memory_percent"] = "cpu_percent",
):
    return system_service.get_top_processes(limit, sort_by)

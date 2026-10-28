from pydantic import BaseModel, EmailStr, Field


class CpuInfo(BaseModel):
    logical_cpus: int | None
    physical_cores: int | None
    usage_percent: float
    per_core_percent: list[float]
    load_avg: list[float]
    freq_mhz: float | None


class MemoryInfo(BaseModel):
    total_gib: float
    available_gib: float
    used_gib: float
    usage_percent: float
    swap_total_gib: float
    swap_used_gib: float
    swap_percent: float


class DiskInfo(BaseModel):
    mountpoint: str
    device: str
    fstype: str
    total_gib: float
    used_gib: float
    free_gib: float
    usage_percent: float


class NetworkInfo(BaseModel):
    bytes_sent_mb: float
    bytes_recv_mb: float
    packets_sent: int
    packets_recv: int
    errors_in: int
    errors_out: int
    connections: int | None


class ProcessInfo(BaseModel):
    pid: int
    name: str | None
    username: str | None
    cpu_percent: float | None
    memory_percent: float | None


class HostInfo(BaseModel):
    hostname: str
    os: str
    platform: str
    boot_time: str
    uptime_seconds: int


class SystemSnapshot(BaseModel):
    host: HostInfo
    cpu: CpuInfo
    memory: MemoryInfo
    disks: list[DiskInfo]
    network: NetworkInfo


class HealthStatus(BaseModel):
    status: str  # ok | warning | critical
    alerts: list[str]


class Sample(BaseModel):
    node: str
    ts: float
    cpu: float | None
    mem: float | None
    disk: float | None
    load1: float | None
    net_sent_mb: float | None
    net_recv_mb: float | None


class AlertRecord(BaseModel):
    id: int
    node: str
    ts: float
    level: str
    message: str
    emailed: bool


class FileEvent(BaseModel):
    id: int
    ts: float
    event: str
    path: str
    is_dir: bool


class ServerIn(BaseModel):
    # restricted charset: the name ends up in email subjects
    name: str = Field(pattern=r"^[A-Za-z0-9._-]{1,40}$")
    url: str = Field(max_length=300)  # base URL of the remote monitor, e.g. https://vps.example.com
    api_key: str = Field(default="", max_length=200)
    enabled: bool = True


class RegisterIn(BaseModel):
    email: EmailStr


class VerifyIn(BaseModel):
    email: EmailStr
    code: str = Field(max_length=100)


class KeyOut(BaseModel):
    api_key: str
    note: str = "Store this key now. It is shown only once."


class Me(BaseModel):
    id: int
    email: str | None
    is_admin: bool


class ServerOut(BaseModel):
    id: int
    name: str
    url: str
    enabled: bool

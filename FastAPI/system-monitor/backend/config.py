import socket

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Run from backend/, the shared .env lives one level up (later files win)
    model_config = SettingsConfigDict(env_file=("../.env", ".env"), extra="ignore")

    node_name: str = socket.gethostname()
    api_key: str = ""  # empty = auth disabled (dev only)

    db_path: str = "monitor.db"
    sample_interval: int = 60  # seconds between samples
    retention_days: int = 7

    # Email alerts
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = ""
    smtp_ssl: bool = False  # True = implicit SSL (465), False = STARTTLS (587)
    alert_to: str = ""  # comma separated recipients
    alert_cooldown: int = 1800  # seconds before re-sending an unchanged alert

    # Admin login with email + password (in addition to the API_KEY, which stays for machine access)
    admin_email: str = ""
    admin_password: str = ""  # at least 12 characters; hashed in the DB, changing it logs the admin out
    admin_session_hours: int = 12
    login_max_failures: int = 5  # failed logins per IP before a lockout
    login_lock_minutes: int = 15

    # Public / multi-user
    allow_registration: bool = True
    max_servers_per_user: int = 5
    verify_ttl_minutes: int = 30
    register_per_ip_per_hour: int = 5
    allow_private_urls: bool = False  # let non-admin users monitor private/loopback IPs (dev only)

    # Thresholds (warning, critical) in percent
    cpu_warn: float = 80
    cpu_crit: float = 95
    mem_warn: float = 80
    mem_crit: float = 95
    disk_warn: float = 80
    disk_crit: float = 90

    # Disks to report as "label=path" pairs, comma separated, e.g. "/=/host,/data=/host/mnt/data".
    # Empty = auto-detect partitions. Needed in Docker, where partitions are the container's own.
    disk_paths: str = ""

    # File watching
    watch_paths: str = ""  # comma separated
    watch_email: bool = False

    @property
    def recipients(self) -> list[str]:
        return [a.strip() for a in self.alert_to.split(",") if a.strip()]

    @property
    def disk_list(self) -> list[tuple[str, str]]:
        pairs = []
        for item in self.disk_paths.split(","):
            item = item.strip()
            if not item:
                continue
            label, _, path = item.partition("=")
            pairs.append((label.strip(), (path or label).strip()))
        return pairs

    @property
    def watch_list(self) -> list[str]:
        return [p.strip() for p in self.watch_paths.split(",") if p.strip()]


settings = Settings()

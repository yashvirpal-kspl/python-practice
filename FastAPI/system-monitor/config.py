import socket

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

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

    # File watching
    watch_paths: str = ""  # comma separated
    watch_email: bool = False

    @property
    def recipients(self) -> list[str]:
        return [a.strip() for a in self.alert_to.split(",") if a.strip()]

    @property
    def watch_list(self) -> list[str]:
        return [p.strip() for p in self.watch_paths.split(",") if p.strip()]


settings = Settings()

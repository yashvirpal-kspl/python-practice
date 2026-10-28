import ipaddress
import socket
from urllib.parse import urlparse


def check_url(url: str):
    """Reject URLs that could be used to reach internal services (SSRF).

    Raises ValueError if the URL is not http(s) or resolves to a non-public address.
    """
    parts = urlparse(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise ValueError("URL must be http(s) with a hostname")
    try:
        infos = socket.getaddrinfo(parts.hostname, parts.port or (443 if parts.scheme == "https" else 80))
    except socket.gaierror:
        raise ValueError("Hostname does not resolve")
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if not ip.is_global:
            raise ValueError("URL resolves to a private or reserved address")

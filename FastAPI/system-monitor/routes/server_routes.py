import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from config import settings
from db import connect
from models.monitor import ServerIn, ServerOut
from netguard import check_url
from security import Principal, get_principal
from services import collector

router = APIRouter(prefix="/servers", tags=["servers"])


@router.get("", response_model=list[ServerOut])
def list_servers(p: Principal = Depends(get_principal)):
    return collector.list_servers(user_id=p.id)


@router.post("", response_model=ServerOut, status_code=201)
def add_server(body: ServerIn, p: Principal = Depends(get_principal)):
    if not p.is_admin:
        if not settings.allow_private_urls:
            try:
                check_url(body.url)
            except ValueError as e:
                raise HTTPException(422, str(e))
        if len(collector.list_servers(user_id=p.id)) >= settings.max_servers_per_user:
            raise HTTPException(409, f"Limit of {settings.max_servers_per_user} servers reached")
    try:
        with connect() as c:
            cur = c.execute(
                "INSERT INTO servers (user_id, name, url, api_key, enabled) VALUES (?,?,?,?,?)",
                (p.id, body.name, body.url, body.api_key, int(body.enabled)),
            )
            new_id = cur.lastrowid
    except sqlite3.IntegrityError:
        raise HTTPException(409, f"Server '{body.name}' already exists")
    return {"id": new_id, "name": body.name, "url": body.url, "enabled": body.enabled}


@router.delete("/{name}", status_code=204)
def remove_server(name: str, p: Principal = Depends(get_principal)):
    with connect() as c:
        if c.execute("DELETE FROM servers WHERE user_id=? AND name=?", (p.id, name)).rowcount == 0:
            raise HTTPException(404, "Server not found")

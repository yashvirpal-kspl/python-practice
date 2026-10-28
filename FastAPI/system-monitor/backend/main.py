import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from db import init_db
from routes.admin_routes import router as admin_routes
from routes.auth_routes import router as auth_routes
from routes.history_routes import router as history_routes
from routes.observers import router as file_routes
from routes.server_routes import router as server_routes
from routes.system_routes import router as system_routes
from routes.user_routes import router as user_routes
from services import admin_auth, observer
from services.collector import run_collector

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    admin_auth.sync_admin()
    observer.start()
    task = asyncio.create_task(run_collector())
    yield
    task.cancel()
    observer.stop()


app = FastAPI(
    title="VPS Monitor",
    description="Monitors this server (and optionally others) with history, email alerts and file watching",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {"message": "Welcome to VPS Monitor API"}


app.include_router(user_routes)
app.include_router(auth_routes)
app.include_router(admin_routes)
app.include_router(system_routes)
app.include_router(history_routes)
app.include_router(server_routes)
app.include_router(file_routes)

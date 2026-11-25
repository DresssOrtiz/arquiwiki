from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import init_db
from app.routers import fuentes, paginas


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="ArquiWiki API",
    version="1.0.0",
    description="CRUD de las entidades Fuente y Página, con su relación N:M.",
    lifespan=lifespan,
)
app.include_router(fuentes.router)
app.include_router(paginas.router)


@app.get("/health", tags=["salud"])
def health():
    return {"status": "ok"}

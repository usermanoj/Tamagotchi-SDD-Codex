from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.db.session import initialize_database

settings = get_settings()

app = FastAPI(
    title="Tiny Tamagotchi API",
    version="0.1.0",
    description="Backend-backed persistence and simulation for ChuChu.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    initialize_database()


app.include_router(api_router, prefix="/api/v1")

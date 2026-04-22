from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    project_root: Path
    database_url: str
    cors_origins: list[str]
    tick_interval_seconds: int = 2
    offline_decay_cap_seconds: int = 28_800


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    project_root = Path(__file__).resolve().parents[2]
    database_path = project_root / "data" / "chuchu.db"
    cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3200").split(",")

    return Settings(
        project_root=project_root,
        database_url=os.getenv("DATABASE_URL", f"sqlite:///{database_path.as_posix()}"),
        cors_origins=[origin.strip() for origin in cors_origins if origin.strip()],
    )

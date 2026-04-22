from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class ActionRequest(BaseModel):
    action: Literal["feed", "play", "rest"]


class PetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    hunger: int
    happiness: int
    energy: int
    status: Literal["normal", "sick", "evolved"]
    last_reaction: str
    last_updated_at: datetime
    healthy_streak: int
    total_ticks: int
    needs_attention: bool
    critical_vitals: list[str]
    evolution_progress: int
    evolution_target: int
    tick_interval_seconds: int

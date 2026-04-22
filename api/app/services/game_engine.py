from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Literal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.pet import Pet

ActionName = Literal["feed", "play", "rest"]
StatusName = Literal["normal", "sick", "evolved"]

MAX_VITAL = 100
MIN_VITAL = 0
LOW_VITAL_THRESHOLD = 25
RECOVERY_THRESHOLD = 40
EVOLUTION_THRESHOLD = 80
EVOLUTION_ACTION_BUFFER_THRESHOLD = 70
EVOLUTION_STREAK_TARGET = 6
ACTION_DELTAS: dict[ActionName, dict[str, int]] = {
    "feed": {"hunger": 30, "happiness": 6, "energy": -1},
    "play": {"happiness": 24, "hunger": -4, "energy": -8},
    "rest": {"energy": 30, "hunger": -2, "happiness": -1},
}
DEFAULT_REACTIONS: dict[ActionName, str] = {
    "feed": "ChuChu munches happily and leans a little closer.",
    "play": "ChuChu spins in a tiny circle and lights up.",
    "rest": "ChuChu settles in and looks recharged.",
}

settings = get_settings()
VALID_STATUSES = {"normal", "sick", "evolved"}
DEFAULT_NAME = "ChuChu"
DEFAULT_VITAL = 92
DEFAULT_REACTION = "ChuChu is awake and waiting for your first move."


@dataclass(frozen=True)
class DerivedState:
    critical_vitals: list[str]
    needs_attention: bool
    evolution_progress: int
    evolution_target: int
    tick_interval_seconds: int


def clamp(value: int) -> int:
    return max(MIN_VITAL, min(MAX_VITAL, value))


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def create_default_pet(now: datetime | None = None) -> Pet:
    current_time = now or utc_now()
    return Pet(
        id=1,
        name=DEFAULT_NAME,
        hunger=DEFAULT_VITAL,
        happiness=DEFAULT_VITAL,
        energy=DEFAULT_VITAL,
        status="normal",
        last_reaction=DEFAULT_REACTION,
        last_updated_at=current_time,
        healthy_streak=0,
        total_ticks=0,
        created_at=current_time,
        updated_at=current_time,
    )


def get_critical_vitals(pet: Pet) -> list[str]:
    critical: list[str] = []
    if pet.hunger <= LOW_VITAL_THRESHOLD:
        critical.append("hunger")
    if pet.happiness <= LOW_VITAL_THRESHOLD:
        critical.append("happiness")
    if pet.energy <= LOW_VITAL_THRESHOLD:
        critical.append("energy")
    return critical


def all_vitals_above(pet: Pet, threshold: int) -> bool:
    return pet.hunger >= threshold and pet.happiness >= threshold and pet.energy >= threshold


def apply_vital_changes(pet: Pet, changes: dict[str, int]) -> None:
    pet.hunger = clamp(pet.hunger + changes.get("hunger", 0))
    pet.happiness = clamp(pet.happiness + changes.get("happiness", 0))
    pet.energy = clamp(pet.energy + changes.get("energy", 0))


def decay_deltas_for_next_tick(next_tick_index: int) -> dict[str, int]:
    # Two-second ticks create a high-pressure, arcade-style care loop.
    return {
        "hunger": -3,
        "happiness": -3,
        "energy": -3,
    }


def is_invalid_loaded_pet(pet: Pet) -> bool:
    return any(
        [
            pet.status not in VALID_STATUSES,
            pet.last_updated_at is None,
            pet.updated_at is None,
            pet.created_at is None,
            pet.hunger is None,
            pet.happiness is None,
            pet.energy is None,
        ]
    )


def reset_pet_fields(pet: Pet, now: datetime) -> Pet:
    pet.name = DEFAULT_NAME
    pet.hunger = DEFAULT_VITAL
    pet.happiness = DEFAULT_VITAL
    pet.energy = DEFAULT_VITAL
    pet.status = "normal"
    pet.last_reaction = DEFAULT_REACTION
    pet.last_updated_at = now
    pet.healthy_streak = 0
    pet.total_ticks = 0
    pet.created_at = now
    pet.updated_at = now
    return pet


def repair_or_reset_loaded_pet(pet: Pet, now: datetime) -> Pet:
    if is_invalid_loaded_pet(pet):
        return reset_pet_fields(pet, now)

    pet.name = DEFAULT_NAME
    pet.hunger = clamp(int(pet.hunger))
    pet.happiness = clamp(int(pet.happiness))
    pet.energy = clamp(int(pet.energy))
    pet.last_updated_at = ensure_utc(pet.last_updated_at)
    pet.updated_at = ensure_utc(pet.updated_at)
    pet.created_at = ensure_utc(pet.created_at)
    pet.healthy_streak = max(0, int(pet.healthy_streak))
    pet.total_ticks = max(0, int(pet.total_ticks))
    return pet


def sync_status(pet: Pet) -> None:
    if pet.status == "evolved":
        return

    critical_count = len(get_critical_vitals(pet))
    if pet.status == "sick":
        if pet.hunger > RECOVERY_THRESHOLD and pet.happiness > RECOVERY_THRESHOLD and pet.energy > RECOVERY_THRESHOLD:
            pet.status = "normal"
        else:
            pet.status = "sick"
        return

    if critical_count >= 2:
        pet.status = "sick"
        return

    pet.status = "normal"


def update_healthy_streak_for_tick(pet: Pet) -> None:
    if pet.status == "evolved":
        pet.healthy_streak = EVOLUTION_STREAK_TARGET
        return

    if all_vitals_above(pet, EVOLUTION_THRESHOLD):
        pet.healthy_streak += 1
        if pet.healthy_streak >= EVOLUTION_STREAK_TARGET:
            pet.status = "evolved"
            pet.last_reaction = "ChuChu has evolved into a calm, radiant companion."
    else:
        pet.healthy_streak = 0


def update_streak_after_action(pet: Pet) -> None:
    if pet.status == "evolved":
        pet.healthy_streak = EVOLUTION_STREAK_TARGET
        return

    if pet.status == "sick":
        pet.healthy_streak = 0
        return

    if all_vitals_above(pet, EVOLUTION_THRESHOLD):
        return

    if all_vitals_above(pet, EVOLUTION_ACTION_BUFFER_THRESHOLD):
        return

    pet.healthy_streak = 0


def reaction_for_current_state(pet: Pet) -> str:
    if pet.status == "evolved":
        return "ChuChu glows softly, completely at ease."
    if pet.status == "sick":
        return "ChuChu looks fragile and needs steady care."
    if all_vitals_above(pet, 90):
        return "ChuChu looks perfectly balanced and a little proud."
    if pet.energy <= 25:
        return "ChuChu blinks slowly and looks ready for a nap."
    if pet.happiness <= 25:
        return "ChuChu wants more attention and a little fun."
    if pet.hunger <= 25:
        return "ChuChu taps the bowl and waits hopefully."
    return "ChuChu is steady, curious, and watching you."


def tick_pet_once(pet: Pet) -> None:
    next_tick_index = pet.total_ticks + 1
    apply_vital_changes(pet, decay_deltas_for_next_tick(next_tick_index))
    pet.total_ticks += 1
    sync_status(pet)
    update_healthy_streak_for_tick(pet)
    pet.last_reaction = reaction_for_current_state(pet)


def apply_elapsed_time(pet: Pet, now: datetime) -> None:
    pet.last_updated_at = ensure_utc(pet.last_updated_at)
    pet.updated_at = ensure_utc(pet.updated_at)

    if now <= pet.last_updated_at:
        pet.updated_at = now
        return

    elapsed_seconds_total = (now - pet.last_updated_at).total_seconds()
    effective_elapsed_seconds = min(elapsed_seconds_total, settings.offline_decay_cap_seconds)
    tick_count = int(effective_elapsed_seconds // settings.tick_interval_seconds)
    consumed_seconds = tick_count * settings.tick_interval_seconds

    for _ in range(tick_count):
        tick_pet_once(pet)

    if elapsed_seconds_total > settings.offline_decay_cap_seconds:
        pet.last_updated_at = now
    else:
        pet.last_updated_at = pet.last_updated_at + timedelta(seconds=consumed_seconds)
    pet.updated_at = now


def build_reaction_for_action(action: ActionName, pet: Pet) -> str:
    if pet.status == "evolved":
        return "Evolved ChuChu accepts the care with graceful confidence."
    if pet.status == "sick":
        if action == "feed":
            return "ChuChu eats slowly, but the color starts to come back."
        if action == "rest":
            return "ChuChu curls up and finally seems a little safer."
        return "ChuChu tries to play, but still needs gentle recovery."
    if pet.hunger >= 95 and action == "feed":
        return "ChuChu was already full, but appreciates the attention."
    if pet.energy >= 95 and action == "rest":
        return "ChuChu stretches more than sleeps, already feeling rested."
    if pet.happiness >= 95 and action == "play":
        return "ChuChu is ecstatic and keeps the game going anyway."
    return DEFAULT_REACTIONS[action]


def derive_state(pet: Pet) -> DerivedState:
    critical_vitals = get_critical_vitals(pet)
    return DerivedState(
        critical_vitals=critical_vitals,
        needs_attention=bool(critical_vitals),
        evolution_progress=min(pet.healthy_streak, EVOLUTION_STREAK_TARGET),
        evolution_target=EVOLUTION_STREAK_TARGET,
        tick_interval_seconds=settings.tick_interval_seconds,
    )


def hydrate_response_fields(pet: Pet) -> Pet:
    pet.last_updated_at = ensure_utc(pet.last_updated_at)
    pet.updated_at = ensure_utc(pet.updated_at)
    derived = derive_state(pet)
    pet.critical_vitals = derived.critical_vitals
    pet.needs_attention = derived.needs_attention
    pet.evolution_progress = derived.evolution_progress
    pet.evolution_target = derived.evolution_target
    pet.tick_interval_seconds = derived.tick_interval_seconds
    return pet


def load_pet(db: Session) -> Pet | None:
    return db.scalar(select(Pet).where(Pet.id == 1))


def persist_pet(db: Session, pet: Pet) -> Pet:
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return hydrate_response_fields(pet)


def get_or_create_active_pet(db: Session, now: datetime | None = None) -> Pet:
    current_time = now or utc_now()
    pet = load_pet(db)
    if pet is None:
        pet = create_default_pet(current_time)
        return persist_pet(db, pet)

    pet = repair_or_reset_loaded_pet(pet, current_time)
    apply_elapsed_time(pet, current_time)
    pet.last_reaction = reaction_for_current_state(pet)
    return persist_pet(db, pet)


def apply_action(db: Session, action: ActionName, now: datetime | None = None) -> Pet:
    current_time = now or utc_now()
    pet = load_pet(db)
    if pet is None:
        pet = create_default_pet(current_time)
        db.add(pet)
        db.commit()
        db.refresh(pet)

    pet = repair_or_reset_loaded_pet(pet, current_time)
    apply_elapsed_time(pet, current_time)
    apply_vital_changes(pet, ACTION_DELTAS[action])
    sync_status(pet)
    update_streak_after_action(pet)
    if pet.status != "evolved" and all_vitals_above(pet, EVOLUTION_THRESHOLD):
        remaining_ticks = max(1, EVOLUTION_STREAK_TARGET - pet.healthy_streak)
        tick_label = "tick" if remaining_ticks == 1 else "ticks"
        pet.last_reaction = f"ChuChu is in the evolution zone. Hold the balance for {remaining_ticks} more {tick_label}."
    elif pet.status != "evolved" and pet.healthy_streak > 0 and all_vitals_above(pet, EVOLUTION_ACTION_BUFFER_THRESHOLD):
        pet.last_reaction = "ChuChu is still on track. Lift every vital back above 80 before the next tick."
    else:
        pet.last_reaction = build_reaction_for_action(action, pet)
    pet.last_updated_at = current_time
    pet.updated_at = current_time
    return persist_pet(db, pet)


def reset_pet(db: Session, now: datetime | None = None) -> Pet:
    current_time = now or utc_now()
    pet = load_pet(db)
    if pet is None:
        pet = create_default_pet(current_time)
    else:
        pet = reset_pet_fields(pet, current_time)
    return persist_pet(db, pet)

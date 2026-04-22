from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.pet import ActionRequest, PetResponse
from app.services.game_engine import apply_action, get_or_create_active_pet, reset_pet

router = APIRouter()


@router.get("/pet", response_model=PetResponse)
def read_pet(db: Session = Depends(get_db)) -> PetResponse:
    pet = get_or_create_active_pet(db, now=datetime.now(timezone.utc))
    return PetResponse.model_validate(pet)


@router.post("/pet/actions", response_model=PetResponse)
def perform_action(payload: ActionRequest, db: Session = Depends(get_db)) -> PetResponse:
    pet = apply_action(db, action=payload.action, now=datetime.now(timezone.utc))
    return PetResponse.model_validate(pet)


@router.post("/pet/reset", response_model=PetResponse)
def reset_active_pet(db: Session = Depends(get_db)) -> PetResponse:
    pet = reset_pet(db, now=datetime.now(timezone.utc))
    return PetResponse.model_validate(pet)

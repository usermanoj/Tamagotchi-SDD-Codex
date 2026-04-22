from fastapi import APIRouter

from app.api.routes.pet import router as pet_router

api_router = APIRouter()
api_router.include_router(pet_router, tags=["pet"])

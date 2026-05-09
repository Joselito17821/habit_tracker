from fastapi import APIRouter

from app.api.routes import predictor, habits

router = APIRouter()
router.include_router(predictor.router, tags=["predictor"], prefix="/v1")
router.include_router(habits.router, tags=["habits"], prefix="/v1/habits")
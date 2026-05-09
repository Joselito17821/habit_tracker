from fastapi import APIRouter

router = APIRouter()


@router.get("/health", name="health:check")
async def health():
    return {"status": "ok"}
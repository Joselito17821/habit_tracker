from contextlib import asynccontextmanager

from app.api.routes.api import router as api_router
from app.core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from app.db import Base, engine
from fastapi import FastAPI
from loguru import logger
from sqlalchemy.exc import OperationalError


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError:
        logger.exception("failed to initialize database")
    yield


def get_application() -> FastAPI:
    application = FastAPI(
        title=PROJECT_NAME,
        debug=DEBUG,
        version=VERSION,
        lifespan=lifespan
    )
    application.include_router(api_router, prefix=API_PREFIX)
    return application


app = get_application()
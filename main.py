from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routers import auth_router, competition_router, entry_router, user_router

src = FastAPI()

src.include_router(auth_router.auth_router, prefix="/auth", tags=["Authentication"])
src.include_router(user_router.user_router, prefix="/user", tags=["User"])
src.include_router(
    competition_router.competition_router, prefix="/competition", tags=["Competition"]
)
src.include_router(entry_router.entry_router, prefix="/entry", tags=["Entry"])

src.mount("/static", StaticFiles(directory="static"), name="static")

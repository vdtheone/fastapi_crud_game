from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routers import user_router, competition_router, entry_router

src = FastAPI()
src.mount("/static", StaticFiles(directory="static"), name="static")

src.include_router(user_router.user_router, prefix='/user')
src.include_router(competition_router.competition_router, prefix='/competition')
src.include_router(entry_router.entry_router, prefix='/entry')

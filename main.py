from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routers import auth_router
from src.routers import competition_router
from src.routers import entry_router
from src.routers import user_router

src = FastAPI()

src.include_router(user_router.user_router, prefix='/user',tags=["user"])
src.include_router(competition_router.competition_router, prefix='/competition', tags=["competition"])
src.include_router(entry_router.entry_router, prefix='/entry', tags=["entry"])
src.include_router(auth_router.auth_router, prefix='/auth', tags=["Authentication"])

src.mount("/static", StaticFiles(directory="static"), name="static")
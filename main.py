from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import user_router, competition_router, entry_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router.user_router, prefix='/user')
app.include_router(competition_router.competition_router, prefix='/competition')
app.include_router(entry_router.entry_router, prefix='/entry')

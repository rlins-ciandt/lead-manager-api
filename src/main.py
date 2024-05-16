from os import getenv
from fastapi import FastAPI, APIRouter

from views.lead import lead_router
from views.auth import auth_router

app = FastAPI()
router = APIRouter()

app.include_router(lead_router)
app.include_router(auth_router)

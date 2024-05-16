from asyncio import gather

from fastapi import APIRouter, Depends, File, Form, HTTPException

from schemas import (
     ErrorOutput,
)
from services.auth import AuthService

auth_router = APIRouter(prefix='/auth')

auth_service = AuthService()

@auth_router.post('/token', responses={400: {'model': ErrorOutput}})
async def login():
    try:
        token = auth_service.get_access_token()
        return {"access_token": token, "token_type": "bearer"}    
    except Exception as error:
        raise HTTPException(400, detail=str(error))

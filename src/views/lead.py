from asyncio import gather
from typing import Annotated, List

from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from schemas import (
    LeadCreateInput, StandardOutput, ErrorOutput, LeadListOutput
)
from services.auth import AuthService
from services.lead import LeadService

lead_router = APIRouter(prefix='/lead')

lead_service = LeadService()
# accept only max 2MB file size
maximum_size = 2 * 1024 * 1024


@lead_router.post('/', description='Creates Lead', response_model=StandardOutput)
async def post_lead( file: Annotated[UploadFile, File()], user_input: Annotated[str, Form()]):

    if file.content_type != "application/pdf":
        raise HTTPException(400,detail="Invalid document type")
    elif file.size > maximum_size:
        raise HTTPException(400,detail="File size too large")
        
    try:
        lead = LeadCreateInput.model_validate_json(user_input)

        await lead_service.create_lead(
            first_name=lead.first_name,
            last_name=lead.last_name,
            email=lead.email,
            resume_file=file.file.read()
        )
        return StandardOutput(message='Application Received. We will contact you soon.') 
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@lead_router.patch('/{email}', responses={400: {'model': ErrorOutput}})
async def mark_as_reached(email: str, _: Annotated[None, Depends(AuthService.secure)]):
    try:
        return await lead_service.mark_as_reached(email)
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@lead_router.delete('/delete/{lead_id}', response_model=StandardOutput, responses={400: {'model': ErrorOutput}})
async def delete_lead(lead_id: int, _: Annotated[None, Depends(AuthService.secure)]):
    try:
        await lead_service.delete_lead(lead_id)
        return StandardOutput(message='Lead deleted') 
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@lead_router.get('/list', response_model=List[LeadListOutput], responses={400: {'model': ErrorOutput}})
async def list_lead(_: Annotated[None, Depends(AuthService.secure)]):
    try:
        return await lead_service.list_leads()
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    

@lead_router.get('/{email}', responses={400: {'model': ErrorOutput}})
async def get_lead(email: str, _: Annotated[None, Depends(AuthService.secure)]):
    try:
        return await lead_service.get_by_email(email)
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@lead_router.get('/resume/{email}', responses={400: {'model': ErrorOutput}})
async def get_resume(email: str, _: Annotated[None, Depends(AuthService.secure)]):
    try:
        base64_resume_file =  await lead_service.get_resume_by_email(email)

        return Response(content=base64_resume_file, 
                        media_type="application/octet-stream", 
                        headers={"Content-Disposition": f"attachment; filename={email}.pdf"})    
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
from pydantic import BaseModel
from typing import List


class LeadCreateInput(BaseModel):
    first_name: str
    last_name: str
    email: str


class StandardOutput(BaseModel):
    message: str

class ErrorOutput(BaseModel):
    detail: str

class LeadListOutput(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    status: str

    class Config:
        orm_mode = True

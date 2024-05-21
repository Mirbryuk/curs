from pydantic import BaseModel
from typing import Optional

class Application(BaseModel):
    id: int
    photo: bytes
    phone_number: str
    longitude: float
    latitude: float
    description: str

    class Config:
        orm_mode = True

class ApplicationCreate(BaseModel):
    photo: bytes
    phone_number: str
    longitude: float
    latitude: float
    description: str

class Message(BaseModel):
    id: int
    phone_number: str
    name: str
    message: str

    class Config:
        orm_mode = True

class MessageCreate(BaseModel):
    phone_number: str
    name: str
    message: str

class Statistics(BaseModel):
    total_users: int
    total_applications: int
    completed_applications: int
    last_updated: Optional[str]

    class Config:
        orm_mode = True

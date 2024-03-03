from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Contact(BaseModel):
    phoneNumber: str | None
    email: str | None


class ContactDetail(BaseModel):
    phoneNumber: str
    id: int
    email: str
    linkedId: Optional[int] = None
    linkPrecedence: Optional[str] = "primary"
    createdAt: datetime
    updatedAt: datetime
    deletedAt: Optional[datetime] = None

    class Config:
        orm_mode = True


class ContactResponse(BaseModel):
    primaryContatctId: int
    emails: list
    phoneNumbers: list
    secondaryContactIds: list


class ContactCreate(BaseModel):
    phoneNumber: str
    email: str
    linkedId: Optional[int] = None
    linkPrecedence: Optional[str] = "primary"

    class Config:
        orm_mode = True

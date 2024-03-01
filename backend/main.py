from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

app = FastAPI()


class Contact(BaseModel):
    phoneNumber: str
    email: str


class ContactDetail(BaseModel):
    phoneNumber: str
    id: int
    email: str
    linkedId: Optional[int] = None
    linkPrecedence: Optional[str] = "primary"
    createdAt: datetime
    updatedAt: datetime
    deletedAt: Optional[datetime] = None


existing_contacts = []


@app.post("/identity")
async def root(data: Contact):
    detail_data = ContactDetail(
        phoneNumber=data.phoneNumber,
        email=data.email,
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
        id=len(existing_contacts) + 1,
    )
    if any(
        contact.phoneNumber == detail_data.phoneNumber for contact in existing_contacts
    ) and any(contact.email != detail_data.email for contact in existing_contacts):
        for contact in existing_contacts:
            if (
                contact.phoneNumber == detail_data.phoneNumber
                and detail_data.linkPrecedence == "primary"
            ):
                detail_data.linkPrecedence = "secondary"
                detail_data.linkedId = contact.id
    elif any(
        contact.email == detail_data.email for contact in existing_contacts
    ) and any(
        contact.phoneNumber != detail_data.phoneNumber for contact in existing_contacts
    ):
        for contact in existing_contacts:
            if (
                contact.email == detail_data.email
                and detail_data.linkPrecedence == "primary"
            ):
                detail_data.linkPrecedence = "secondary"
                detail_data.linkedId = contact.id
    else:
        detail_data.linkPrecedence = "primary"
        detail_data.linkedId = None
        detail_data.createdAt = datetime.now()
        detail_data.updatedAt = datetime.now()
    existing_contacts.append(detail_data)
    print(existing_contacts)

    return {"message": existing_contacts}


@app.get("/identity")
async def root(data: Contact):
    # if any(contact.phoneNumber == data.phoneNumber for contact in existing_contacts) and \
    #     any(contact.email != data.email for contact in existing_contacts):
    #         data.linkPrecedence = 'secondary'
    #         for contact in existing_contacts:
    #             if contact.phoneNumber == data.phoneNumber and data.linkPrecedence== 'primary':
    #                 data.linkedId = contact.id
    return {"message": existing_contacts}

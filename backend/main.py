from fastapi import FastAPI, Depends
from datetime import datetime
import models
import schema
from sqlalchemy.orm import Session
from database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


existing_contacts = []


@app.post("/identity")
async def root(data: schema.Contact, db: Session = Depends(get_db)):
    contacts_with_input_email = (
        db.query(models.Contact)
        .filter(
            models.Contact.email == data.email,
            models.Contact.phone_number != data.phoneNumber,
        )
        .first()
    )
    contacts_with_input_phone = (
        db.query(models.Contact)
        .filter(
            models.Contact.phone_number == data.phoneNumber,
            models.Contact.email != data.email,
        )
        .first()
    )
    contacts_with_input_email_and_phone = (
        db.query(models.Contact)
        .filter(
            models.Contact.phone_number == data.phoneNumber,
            models.Contact.email == data.email,
        )
        .first()
    )

    if contacts_with_input_phone and not contacts_with_input_email:
        db_new_contact = models.Contact(
            email=data.email,
            phone_number=data.phoneNumber,
            link_precedence="secondary",
            linked_id=contacts_with_input_phone[0].id,
        )
        db.add(db_new_contact)
        db.commit()
        db.refresh(db_new_contact)
    elif contacts_with_input_email and not contacts_with_input_phone:
        print("00000", contacts_with_input_email.id)
        db_new_contact = models.Contact(
            email=data.email,
            phone_number=data.phoneNumber,
            link_precedence="secondary",
            linked_id=contacts_with_input_email.id,
        )
        db.add(db_new_contact)
        db.commit()
        db.refresh(db_new_contact)
    elif contacts_with_input_email_and_phone:
        return {"message": contacts_with_input_email_and_phone}
    else:
        db_new_contact = models.Contact(
            email=data.email, phone_number=data.phoneNumber, link_precedence="primary"
        )
        db.add(db_new_contact)
        db.commit()
        db.refresh(db_new_contact)
    return {"message": db_new_contact}


@app.get("/identity")
async def root(db: Session = Depends(get_db)):
    contacts_with_input_email = db.query(models.Contact).all()
    # if any(contact.phoneNumber == data.phoneNumber for contact in existing_contacts) and \
    #     any(contact.email != data.email for contact in existing_contacts):
    #         data.linkPrecedence = 'secondary'
    #         for contact in existing_contacts:
    #             if contact.phoneNumber == data.phoneNumber and data.linkPrecedence== 'primary':
    #                 data.linkedId = contact.id
    return {"message": contacts_with_input_email}

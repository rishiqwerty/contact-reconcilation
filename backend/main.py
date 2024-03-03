from fastapi import FastAPI, Depends
from datetime import datetime
import models
import schema
from sqlalchemy import update
from sqlalchemy.orm import Session
from database import SessionLocal, engine, get_db
import crud

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


# Oldest entry will be treated as Primary rest will be secondary
# COntacts will be linked if either of the phone number or email is common
#
# Dependency


existing_contacts = []


@app.post("/identify")
async def root(data: schema.Contact, db: Session = Depends(get_db)):
    response = crud.get_contact(db=db, data=data)
    # response = {
    #     "contact": {"emails": [], "phoneNumbers": [], "secondaryContactIds": []}
    # }

    # # Get contacts with provided email not = phone number
    # contacts_with_input_email = db.query(models.Contact).filter(
    #     models.Contact.email == data.email,
    #     models.Contact.phone_number != data.phoneNumber,
    # )
    # # Get contacts with provided phone_number not = email
    # contacts_with_input_phone = db.query(models.Contact).filter(
    #     models.Contact.phone_number == data.phoneNumber,
    #     models.Contact.email != data.email,
    # )
    # # Get contacts with provided email as well as phone
    # contacts_with_input_email_and_phone = (
    #     db.query(models.Contact)
    #     .filter(
    #         models.Contact.phone_number == data.phoneNumber,
    #         models.Contact.email == data.email,
    #     )
    #     .first()
    # )
    # print(
    #     "DET",
    #     contacts_with_input_email.first(),
    #     contacts_with_input_phone.first(),
    #     contacts_with_input_email_and_phone,
    #     data,
    # )
    # # If both the email and contact match then just print the
    # if (
    #     contacts_with_input_email_and_phone
    #     or (data.phoneNumber and not data.email)
    #     or (not data.phoneNumber and data.email)
    # ):
    #     result = contacts_with_input_email
    # # Doing checks if contacts with phone and not contact with email
    # elif contacts_with_input_email.first() and contacts_with_input_phone.first():
    #     # Fix this
    #     contacts_with_input_phone = contacts_with_input_phone.order_by(
    #         models.Contact.created_at.asc()
    #     ).first()

    #     contacts_with_input_phone = contacts_with_input_phone.order_by(
    #         models.Contact.created_at.asc()
    #     ).first()
    #     if contacts_with_input_email.created_at > contacts_with_input_phone.created_at:
    #         contacts_with_input_phone.link_precedence = "primary"
    #         contacts_with_input_email.link_precedence = "secondary"
    #         db.commit()
    #     db.refresh(contacts_with_input_email)
    #     db.refresh(contacts_with_input_phone)

    # elif contacts_with_input_phone.first() and not contacts_with_input_email.first():
    #     db_new_contact = models.Contact(
    #         email=data.email,
    #         phone_number=data.phoneNumber,
    #         link_precedence="secondary",
    #         linked_id=contacts_with_input_phone[0].id,
    #     )
    #     db.add(db_new_contact)
    #     db.commit()
    #     db.refresh(db_new_contact)
    #     db.refresh(contacts_with_input_phone)
    # elif contacts_with_input_email.first() and not contacts_with_input_phone.first():
    #     db_new_contact = models.Contact(
    #         email=data.email,
    #         phone_number=data.phoneNumber,
    #         link_precedence="secondary",
    #         linked_id=contacts_with_input_email.id,
    #     )
    #     db.add(db_new_contact)
    #     db.commit()
    #     db.refresh(db_new_contact)
    #     db.refresh(contacts_with_input_email)
    # else:
    #     if data.email and data.phoneNumber:
    #         db_new_contact = models.Contact(
    #             email=data.email,
    #             phone_number=data.phoneNumber,
    #             link_precedence="primary",
    #         )
    #         db.add(db_new_contact)
    #         print(db_new_contact)
    #         db.commit()
    #         db.refresh(db_new_contact)
    #         contacts_with_input_email_and_phone = db_new_contact

    # if contacts_with_input_email_and_phone:
    #     if contacts_with_input_email_and_phone.link_precedence == "primary":
    #         response["contact"][
    #             "primaryContatctId"
    #         ] = contacts_with_input_email_and_phone.id
    #     else:
    #         response["contact"]["secondaryContactIds"].append(
    #             contacts_with_input_email_and_phone.id
    #         )
    #     if (
    #         not contacts_with_input_email_and_phone.phone_number
    #         in response["contact"]["phoneNumbers"]
    #     ):
    #         response["contact"]["phoneNumbers"].append(
    #             contacts_with_input_email_and_phone.phone_number
    #         )
    #     if (
    #         not contacts_with_input_email_and_phone.email
    #         in response["contact"]["emails"]
    #     ):
    #         response["contact"]["emails"].append(
    #             contacts_with_input_email_and_phone.email
    #         )
    # for i in contacts_with_input_email.all():
    #     if i.link_precedence == "primary":
    #         response["contact"]["primaryContatctId"] = i.id
    #     else:
    #         response["contact"]["secondaryContactIds"].append(i.id)

    #     if not i.email in response["contact"]["emails"]:
    #         response["contact"]["emails"].append(i.email)
    #     if not i.phone_number in response["contact"]["phoneNumbers"]:
    #         response["contact"]["phoneNumbers"].append(i.phone_number)

    # for i in contacts_with_input_phone.all():
    #     if i.link_precedence == "primary":
    #         response["contact"]["primaryContatctId"] = i.id
    #     else:
    #         response["contact"]["secondaryContactIds"].append(i.id)
    #     if not i.email in response["contact"]["emails"]:
    #         response["contact"]["emails"].append(i.email)
    #     if not i.phone_number in response["contact"]["phoneNumbers"]:
    #         response["contact"]["phoneNumbers"].append(i.phone_number)

    return response


@app.get("/identify")
async def root(db: Session = Depends(get_db)):
    contacts_with_input_email = db.query(models.Contact).all()
    # if any(contact.phoneNumber == data.phoneNumber for contact in existing_contacts) and \
    #     any(contact.email != data.email for contact in existing_contacts):
    #         data.linkPrecedence = 'secondary'
    #         for contact in existing_contacts:
    #             if contact.phoneNumber == data.phoneNumber and data.linkPrecedence== 'primary':
    #                 data.linkedId = contact.id
    return {"message": contacts_with_input_email}

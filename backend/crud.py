from sqlalchemy.orm import Session
import models
import schema


def create_new_contact(
    db: Session, email: str, phone_number: str, precedence: str, linked_id: int = None
):
    db_new_contact = models.Contact(
        email=email,
        phone_number=phone_number,
        link_precedence=precedence,
        linked_id=linked_id,
    )
    db.add(db_new_contact)
    db.commit()
    db.refresh(db_new_contact)
    return db_new_contact


def assign_data_to_dict(db: Session, contact_detail, response):
    for i in contact_detail:
        if i.link_precedence == "primary":
            response["contact"]["primaryContatctId"] = i.id
        else:
            if i.id not in response["contact"]["secondaryContactIds"]:
                response["contact"]["secondaryContactIds"].append(i.id)
        if not i.email in response["contact"]["emails"]:
            response["contact"]["emails"].append(i.email)
        if not i.phone_number in response["contact"]["phoneNumbers"]:
            response["contact"]["phoneNumbers"].append(i.phone_number)
    return response


def get_primary_contact_and_its_associated_contacts(
    db: Session,
    contacts_detail,
):
    linked_contacts, contacts_with_input_email_and_phone = [], []
    if contacts_detail.first():
        # If there are contacts with provided phonenumber/email then get the primary contact and get its associated secondary contacts
        primary_contacts = contacts_detail.filter(
            models.Contact.link_precedence == "primary"
        ).first()
        if not primary_contacts:
            get_primary_contact_id = (
                contacts_detail.filter(models.Contact.link_precedence == "secondary")
                .first()
                .linked_id
            )
        else:
            get_primary_contact_id = primary_contacts.id

        linked_contacts = (
            db.query(models.Contact)
            .filter(models.Contact.linked_id == get_primary_contact_id)
            .all()
        )
        contacts_with_input_email_and_phone = (
            db.query(models.Contact)
            .filter(models.Contact.id == get_primary_contact_id)
            .first()
        )
    return linked_contacts, contacts_with_input_email_and_phone


def get_contact(db: Session, data: schema.Contact):
    response = {
        "contact": {"emails": [], "phoneNumbers": [], "secondaryContactIds": []}
    }
    linked_contacts = []

    # Get contacts with provided email not = phone number
    contacts_with_input_email = db.query(models.Contact).filter(
        models.Contact.email == data.email,
        models.Contact.phone_number != data.phoneNumber,
    )
    # Get contacts with provided phone_number not = email
    contacts_with_input_phone = db.query(models.Contact).filter(
        models.Contact.phone_number == data.phoneNumber,
        models.Contact.email != data.email,
    )
    # Get contacts with provided email as well as phone
    contacts_with_input_email_and_phone = (
        db.query(models.Contact)
        .filter(
            models.Contact.phone_number == data.phoneNumber,
            models.Contact.email == data.email,
        )
        .first()
    )

    # If both the email and phone number match/ email/phone number is not provided then dont do anything
    if (
        contacts_with_input_email_and_phone
        or (data.phoneNumber and not data.email)
        or (not data.phoneNumber and data.email)
    ):
        if data.phoneNumber and not data.email:
            linked_contacts, contacts_with_input_email_and_phone = (
                get_primary_contact_and_its_associated_contacts(
                    db, contacts_with_input_phone
                )
            )
        elif not data.phoneNumber and data.email:
            linked_contacts, contacts_with_input_email_and_phone = (
                get_primary_contact_and_its_associated_contacts(
                    db, contacts_with_input_email
                )
            )

    # If contacts matching provided email not phone number and contacts matching provided phone number not email
    # Then get list of primary contacts and mark the oldest one as primary and the rest as secondary
    elif contacts_with_input_email.first() and contacts_with_input_phone.first():
        # Checking the oldest contact with the provided email and is marked as primary
        contacts_with_input_email_new = (
            contacts_with_input_email.filter(
                models.Contact.link_precedence == "primary"
            )
            .order_by(models.Contact.created_at.asc())
            .first()
        )

        # Checking the oldest contact with the provided phone number and is marked as primary
        contacts_with_input_phone_new = (
            contacts_with_input_phone.filter(
                models.Contact.link_precedence == "primary"
            )
            .order_by(models.Contact.created_at.asc())
            .first()
        )

        # The older data will be made primary and latest once is marked secondary
        if (
            contacts_with_input_email_new.created_at
            > contacts_with_input_phone_new.created_at
        ):
            contacts_with_input_phone_new.link_precedence = "primary"
            contacts_with_input_email_new.link_precedence = "secondary"
            contacts_with_input_email_new.linked_id = contacts_with_input_phone_new.id
            linked_contacts = (
                db.query(models.Contact)
                .filter(models.Contact.linked_id == contacts_with_input_phone_new.id)
                .all()
            )
        else:
            contacts_with_input_phone_new.link_precedence = "secondary"
            contacts_with_input_email_new.link_precedence = "primary"
            contacts_with_input_phone_new.linked_id = contacts_with_input_email_new.id
            linked_contacts = (
                db.query(models.Contact)
                .filter(models.Contact.linked_id == contacts_with_input_email_new.id)
                .all()
            )

        db.commit()

    # if contacts only matching provided phonenumber then create new contact with the provided data and mark it as secondary
    elif contacts_with_input_phone.first() and not contacts_with_input_email.first():
        db_new_contact = create_new_contact(
            db,
            email=data.email,
            phone_number=data.phoneNumber,
            precedence="secondary",
            linked_id=contacts_with_input_phone[0].id,
        )
        linked_contacts = (
            db.query(models.Contact)
            .filter(models.Contact.linked_id == contacts_with_input_phone[0].id)
            .all()
        )
    # if contacts only matching provided email then create new contact with the provided data and mark it as secondary
    elif contacts_with_input_email.first() and not contacts_with_input_phone.first():
        db_new_contact = create_new_contact(
            db,
            email=data.email,
            phone_number=data.phoneNumber,
            precedence="secondary",
            linked_id=contacts_with_input_email[0].id,
        )
        linked_contacts = (
            db.query(models.Contact)
            .filter(models.Contact.linked_id == contacts_with_input_phone[0].id)
            .all()
        )
    else:
        # if the is all new then create new contact with precedence set as primary
        if data.email and data.phoneNumber:
            db_new_contact = create_new_contact(
                db,
                email=data.email,
                phone_number=data.phoneNumber,
                precedence="primary",
            )
            contacts_with_input_email_and_phone = db_new_contact

    # If the provided data matches with exact entry in table
    if contacts_with_input_email_and_phone:

        if contacts_with_input_email_and_phone.link_precedence == "primary":
            response["contact"][
                "primaryContatctId"
            ] = contacts_with_input_email_and_phone.id
        else:
            response["contact"]["secondaryContactIds"].append(
                contacts_with_input_email_and_phone.id
            )
        if (
            not contacts_with_input_email_and_phone.phone_number
            in response["contact"]["phoneNumbers"]
        ):
            response["contact"]["phoneNumbers"].append(
                contacts_with_input_email_and_phone.phone_number
            )
        if (
            not contacts_with_input_email_and_phone.email
            in response["contact"]["emails"]
        ):
            response["contact"]["emails"].append(
                contacts_with_input_email_and_phone.email
            )

    response = assign_data_to_dict(db, linked_contacts, response)
    # now looping over all email enteries where phonenumber not matching
    response = assign_data_to_dict(db, contacts_with_input_email.all(), response)

    # then looping over all phonenumber enteries where email not matching
    response = assign_data_to_dict(db, contacts_with_input_phone.all(), response)

    return response

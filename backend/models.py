from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from datetime import datetime

from database import Base
from sqlalchemy.orm import validates


class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True)
    email = Column(String, index=True)
    phone_number = Column(String, index=True)
    linked_id = Column(Integer, ForeignKey("contact.id"), nullable=True)
    link_precedence = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    @validates("link_precedence")
    def validate_link_precedence(self, key, address):
        if address not in ["primary", "secondary"]:
            raise ValueError("failed simple email validation")
        return address

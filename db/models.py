import uuid

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    events = relationship("Event")

    def __repr__(self):
        return f"<User(id={self.id})>"


class Event(Base):
    __tablename__ = "event"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    type = Column(String)
    amount = Column(Float)
    client_timestamp = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="events")

    def __repr__(self):
        return f"<Event(id={self.id})>"

import os
import uuid

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import Event, User

load_dotenv()


class BaseDAO:
    """
    Base class for all DAOs.

    Contains common methods for all DAOs.
    """

    @classmethod
    def _db_engine(self):
        return create_engine(
            os.getenv("DATABASE_URL"),
            echo=True,
            future=True,
        )


class UserDAO(BaseDAO):
    """
    Data Access Object for User model
    """

    @classmethod
    def create(self) -> None:
        with Session(self._db_engine()) as session:
            session.add(User())
            session.commit()

    @classmethod
    def get(self, user_id: uuid) -> User:
        with Session(self._db_engine()) as session:
            return session.query(User).filter(User.id == user_id).one()


class EventDAO(BaseDAO):
    """
    Data Access Object for Event model
    """

    @classmethod
    def create(
        self,
        *,
        amount,
        client_timestamp,
        type,
        user_id,
    ) -> None:
        with Session(self._db_engine()) as session:
            session.add(
                Event(
                    **{
                        "amount": amount,
                        "client_timestamp": client_timestamp,
                        "type": type,
                        "user_id": user_id,
                    }
                )
            )
            session.commit()

    @classmethod
    def get_events(
        self,
        user_id: uuid,
        limit: int = 1000,
    ) -> list:
        """
        Get events for a user ordered in descending created_at order.
        """
        with Session(self._db_engine()) as session:
            return (
                session.query(Event)
                .filter(Event.user_id == user_id)
                .order_by(Event.created_at.desc())
                .limit(limit)
                .all()
            )

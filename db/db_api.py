import os
import uuid

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import User

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
    def create(self) -> User:
        with Session(self._db_engine()) as session:
            session.add(User())
            session.commit()

    @classmethod
    def get(self, user_id: uuid) -> User:
        with Session(self._db_engine()) as session:
            return session.query(User).filter(User.id == user_id).one()

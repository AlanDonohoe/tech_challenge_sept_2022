from functools import cache, cached_property
import os
import uuid

from dotenv import load_dotenv
from sqlalchemy import create_engine

# from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from .models import Event, User

load_dotenv()


class BaseDAO:
    # @classmethod
    # # @cached_property
    # def _db_session(self) -> sessionmaker:
    #     # db_engine = self._db_engine
    #     return sessionmaker(
    #         autocommit=False, autoflush=False, bind=self._db_engine()
    #     )

    # private

    @classmethod
    # @cached_property
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
        user = None
        with Session(self._db_engine()) as session:
            user = session.add(User())
            session.commit()

        return user

        # try:
        #     # user = User(id=user_id)
        #     user = self._db_session().add(User())
        #     self._db_session().commit()
        #     self._db_session().refresh(user)
        # finally:
        #     self._db_session().close()

        # return user

    @classmethod
    def get(self, user_id: uuid) -> User:
        try:
            user = (
                self._db_session.query(User).filter(User.id == user_id).one()
            )
        finally:
            self._db_session.close()

        return user

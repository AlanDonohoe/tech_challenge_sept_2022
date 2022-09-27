# # from dotenv import load_dotenv
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os
# import sys


# def __database_url():
#     if __test_env():
#         return os.environ.get("DATABASE_URL_TEST")
#     else:
#         return os.environ.get("DATABASE_URL")


# def __test_env():
#     if "pytest" in sys.modules:
#         return True
#     else:
#         return False


# Base = declarative_base()
# engine = create_engine(__database_url())
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

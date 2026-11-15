"""A separate database for the tests: test.db, emptied before every test."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base

PASSWORD = "kilc-chat-2026"           # every test user has this password

test_engine = create_engine("sqlite:///test.db")
TestSession = sessionmaker(test_engine)


def fresh_db():
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)


def get_test_db():
    with TestSession() as session:
        yield session

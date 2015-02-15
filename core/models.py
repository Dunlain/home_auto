# Built-ins
import datetime
# Stack Packages
from sqlalchemy import Column, Integer, Unicode, DateTime
from sqlalchemy.ext.declarative import declarative_base
# Module Constants
Base = declarative_base()


class User(Base):
    """
    Base user database model.
    Fields:
        name: the username
        password: the user password
        last_logged: most recent time the user logged in
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)
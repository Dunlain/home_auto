# Built-ins
import datetime
# Stack Packages
from sqlalchemy import Column, Integer, Unicode, DateTime, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
# Module Constants
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from zope.sqlalchemy.datamanager import ZopeTransactionExtension

Base = declarative_base()
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

PRIORITY_CHOICES = Enum(
    "low",
    "medium",
    "high",
    name='priority_types'
)


# ======
# Models
# ======

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
    email = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)  # TODO: Make me secure.
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)


class Note(Base):
    """
    Base user-created note model.
    Fields:
        title: the note title
        text: the note text
        parent: the note that this note is in response to
        owner: the user that created this note
        added: the date when this note was created
        expires: if this note will expire there will be a date
    """
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    text = Column(Unicode(512), nullable=False)
    parent = Column(Integer, ForeignKey(id, onupdate="CASCADE", ondelete='CASCADE'), nullable=True)
    owner = Column(Integer, ForeignKey(User.id, onupdate="CASCADE", ondelete='CASCADE'), nullable=False)
    added = Column(DateTime, default=datetime.datetime.utcnow)
    expires = Column(DateTime, nullable=True)


class ListCategory(Base):
    """
    A model by which ``List``s may be categorized.
    Fields:
        name: the category name
    """
    __tablename__ = 'list_categories'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    # TODO: More fields?


class List(Base):
    """
    Base "TODO-style" list.
    Fields:
        name: the list name
        category: the variety of list (ForeignKey)
        priority: the importance of this list
        owner: the primary user of this list
        added: the date when this list was created
    """
    __tablename__ = 'lists'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    category = Column(Integer, ForeignKey(ListCategory.id, onupdate="CASCADE", ondelete="SET NULL"), nullable=True)
    priority = Column(PRIORITY_CHOICES, nullable=True)
    owner = Column(Integer, ForeignKey(User.id, onupdate="CASCADE", ondelete='CASCADE'), nullable=False)


class Item(Base):
    """
    List Item model.
    Fields:
        text: the item's text
        priority: the item's priority (Foreign Key)
        added: the date and time that the item was added
        owner: the item owner (Foreign Key)
    """
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    priority = Column(PRIORITY_CHOICES, nullable=True)
    owner = Column(Integer, ForeignKey(User.id, onupdate="CASCADE", ondelete='CASCADE'), nullable=False)
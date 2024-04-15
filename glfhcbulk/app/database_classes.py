from sqlalchemy import orm, Column, Integer, String, DateTime, Boolean, Index, JSON, Text, DECIMAL
from sqlalchemy.orm import relationship, backref, declared_attr
from sqlalchemy.ext.declarative import declarative_base
from typing import List, TypedDict
from datetime import date

Base = declarative_base()
metadata = Base.metadata


class Base(object):
    """

    Class Base:

    This class serves as a base class for other classes in the application. It contains some generic functionality that is commonly used across different entities.

    Attributes:
    - __tablename__ (declared_attr): This attribute is a special attribute that defines the table name for the class. It uses the class name converted to lowercase as the table name.
    - __table_args__ (dict): This attribute defines additional arguments for the table, such as the MySQL engine to use (InnoDB).
    - attributes (dict): This attribute is a generic attribute map that allows storing additional data that is not in the database.

    Methods:
    - __str__(): This method returns a string representation of the object. It concatenates the class name with the attribute name and value pairs.

    """

    @declared_attr
    def __tablename__(self, cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}

    # this is a generic attribute map that lets you drop random data into the entity so that you can pass data
    # that isn't in the database
    attributes = {}

    def __str__(self):
        elements = [self.__class__.__name__.upper(), ]
        skip = False
        for key, value in self.__dict__.items():
            if skip:
                elements.append("{key}='{value}'".format(key=key, value=value))
            else:
                skip = True
        return ', '.join(elements)


Base = declarative_base(cls=Base)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    created = Column(DateTime)
    title = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    type_id = Column(Integer, nullable=False)


class CollectionRecord(Base):
    __tablename__ = 'collection_record'
    id = Column(Integer, primary_key=True)
    collection_id = Column(Integer, nullable=False)


class CollectionType(Base):
    __tablename__ = 'collection_type'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    table_name = Column(String, nullable=False)
    field_name = Column(String, nullable=False)
    note = Column(String, nullable=True)

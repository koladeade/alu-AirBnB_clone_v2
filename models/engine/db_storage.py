#!/usr/bin/python3
"""
Module for the DBStorage engine
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.state import State
from models.city import City
from models.base_model import Base
import os


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Initializing a DB connection"""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True
        )
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries all objects"""
        if cls:
            objs = self.__session.query(cls).all()
        else:
            objs = self.__session.query(State).all() + self.__session.query(City).all()
        return {f'{type(obj).__name__}.{obj.id}': obj for obj in objs}

    def new(self, obj):
        """Adds object to session"""
        self.__session.add(obj)

    def save(self):
        """Commits changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes object"""
        if obj:
            self.__session.delete(obj)

    def get(self, cls, id):
        """Retrieves object """
        if cls and id:
            key = f"{cls.__name__}.{id}"
            return self.all(cls).get(key)
        return None

    def reload(self):
        """Creates tables and a session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()

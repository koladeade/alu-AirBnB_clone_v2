#!/usr/bin/python3
"""
Module for the DBStorage engine
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.base_model import BaseModel, Base
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
        
        # Create session factory
        self.__session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        Session = scoped_session(self.__session_factory)
        self.__session = Session()

    def all(self, cls=None, id=None):
        """Query on the current database session."""
        if cls is None:
            classes = [User, State, City, Amenity, Place, Review]
            objects = []
            for c in classes:
                objects += self.__session.query(c).all()
        else:
            objects = self.__session.query(cls).all()
            if id is not None:
                return {type(obj).__name__ + "." + obj.id: obj
                        for obj in objects if obj.id == id}
        return {type(obj).__name__ + "." + obj.id: obj
                for obj in objects}
            
    def new(self, obj):
        """Adds object to session"""
        if obj and not self.__session.object_session(obj):
            self.__session.add(obj)

    def save(self):
        """Commits changes"""
        try:
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e

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
        self.__session.close()
        Session = scoped_session(self.__session_factory)
        self.__session = Session()

    def close(self):
        """Closes the session"""
        self.__session.close()
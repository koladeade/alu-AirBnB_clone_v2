#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
import os

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the DBStorage engine"""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        db_url = f'mysql+mysqldb://{user}:{pwd}@{host}/{db}'
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries all objects"""
        objs_list = []
        if cls:
            if isinstance(cls, str):
                try:
                    cls = globals()[cls]
                except KeyError:
                    pass
            if issubclass(cls, Base):
                objs_list = self.__session.query(cls).all()
        else:
            for subclass in Base.__subclasses__():
                objs_list.extend(self.__session.query(subclass).all())
        obj_dict = {}
        for obj in objs_list:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            try:
                del obj.__sa_instance_state
                obj_dict[key] = obj
            except Exception:
                pass
        return obj_dict

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

    def reload(self):
        """Creates tables and a session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
#!/usr/bin/python3
"""JUST A RANDOM LINE"""

from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class DBStorage:
    
    """JUST A RANDOM LINE"""
    
    __engine = None
    __session = None

    def __init__(self):
        """JUST A RANDOM LINE"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST', 'localhost'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """JUST A RANDOM LINE"""
        obj_dict = {}
        classes = ['User', 'State', 'City', 'Amenity', 'Place', 'Review']

        if cls:
            if type(cls) == str:
                cls = eval(cls)
            query = self.__session.query(cls).all()
            for obj in query:
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                obj_dict[key] = obj
        else:
            for c in classes:
                query = self.__session.query(eval(c)).all()
                for obj in query:
                    key = '{}.{}'.format(c, obj.id)
                    obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        """JUST A RANDOM LINE"""
        self.__session.add(obj)

    def save(self):
        """JUST A RANDOM LINE"""
        self.__session.commit()

    def delete(self, obj=None):
        """JUST A RANDOM LINE"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """JUST A RANDOM LINE"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))()

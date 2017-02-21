#! /usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from pyramid.security import Allow, Everyone
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from sqlalchemy import Column, Integer, String, DateTime, BOOLEAN, Text
from sqlalchemy import Numeric, func, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from zope.sqlalchemy import ZopeTransactionExtension

from pyramid_sqlalchemy import BaseObject

#Описание Access list(листов доступа)
class Root(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:editors', 'edit')] #Еcли у view стоит permission = edit, проверяется пользователь 
                                                 #в 'group:editors', через security.groupfinder

    def __init__(self, request):
        pass
#Описание моделей
class User(BaseObject):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    UserName = Column(String, nullable=False)
    UserPass = Column(String, nullable=False)
    LastName = Column(String)
    FirstName = Column(String)
    Email = Column(String)
    VKID = Column(String)
    TelNum = Column(String)

    password_hash = Column(Text)

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password_hash = pwhash.decode('utf8')

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False

    Child = Column(Integer, ForeignKey("Childs.id"))

    def __repr__(self):
        return "<User(%r)>" % (
            self.UserName
        )


class Group(BaseObject):
    __tablename__ = 'Groups'

    id = Column(Integer, primary_key=True)
    GroupName = Column(String, nullable=False)
    VospName = Column(String, nullable=False)

    Child = Column(Integer, ForeignKey("Childs.id"))
    Event = Column(Integer, ForeignKey("Events.id"))

    def __repr__(self):
        return "<Group(%r)>" % (
            self.GroupName
        )


class Event(BaseObject):
    __tablename__ = 'Events'

    id = Column(Integer, primary_key=True)
    EventName = Column(String)#, nullable=False)
    EventDate = Column(DateTime)
    EventTime = Column(String)
    EventPlace = Column(String)

    def __repr__(self):
        return "<Event(%r, %r)>" % (
            self.EventName, self.EventDate
        )


class Child(BaseObject):
    __tablename__ = 'Childs'

    id = Column(Integer, primary_key=True)
    Age = Column(String, nullable=False)
    Name = Column(DateTime, nullable=False)

    def __repr__(self):
        return "<member(%r, %r)>" % (
            self.Name, self.Age
        )
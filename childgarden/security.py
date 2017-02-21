#! /usr/bin/env python
# -*- coding: utf-8 -*-
import bcrypt
from .models import User
from pyramid_sqlalchemy import Session as DBSession

def hash_password(pw):
    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    return pwhash.decode('utf8')

def check_password(pw, hashed_pw):
    expected_hash = hashed_pw.encode('utf8')
    return bcrypt.checkpw(pw.encode('utf8'), expected_hash)


#Добавляем админа в групу разработчиков
GROUPS = {'admin': ['group:editors']}

#Проверяет находится ли пользователь в каких либо группах
def groupfinder(userid, request):
    for user in DBSession.query(User):
        return GROUPS.get(userid, [])
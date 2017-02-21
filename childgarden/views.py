#! /usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.view import view_config, view_defaults
from pyramid_sqlalchemy import Session as DBSession
from models import (
    Event,
    User,
)

import colander
import deform.widget

from .security import (
    hash_password,
    check_password,
)

from pyramid.security import (
    remember,
    forget,
    )

from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

#Представления
@view_defaults(renderer='templates/mytemplate.pt')
class MyViews:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='home', renderer='templates/index.jinja2')
    def home(self):
        return {'project': 'ChildGarden'}

    @view_config(route_name='galery', renderer='templates/foto-galery.jinja2')
    def galery(self):
        return {'project': 'ChildGarden'}

    @view_config(route_name='spisok', renderer='templates/list-group.jinja2')
    def spisok(self):
        return {'project': 'ChildGarden'}

    @view_config(route_name='calendar', renderer='templates/calendar.jinja2')
    def calendar(self):
        events = DBSession.query(Event).order_by(Event.id)
        return {'events':events}

    @view_config(route_name='callback', renderer='templates/callback.jinja2')
    def callback(self):
        return {'project': 'ChildGarden'}
    
    #Доступно только пользователям из группы editors, т.к. permission='edit'
    @view_config(route_name='addEvent', renderer='templates/addEvent.jinja2', permission='edit')
    def addEvent(self):
        request = self.request
        if 'form.submitted' in request.params:
            name = request.params['name']
            date = request.params['date']
            DBSession.add(Event(EventName = name, EventTime = date))
        events = DBSession.query(Event).order_by(Event.id)
        return {'events':events}

    @view_config(route_name='login', renderer='templates/login.jinja2')
    def login(self):
        request = self.request
        login_url = request.route_url('login')
        referrer = request.url
        if referrer == login_url:
            referrer = '/'  
        came_from = request.params.get('came_from', referrer)
        message = ''
        login = ''
        password = ''
        if 'form.submitted' in request.params:
            login = request.params['login']
            password = request.params['password']
            for user in DBSession.query(User):
                if (user.UserName == login):
                    if check_password(password, hash_password(user.UserPass)):
                        headers = remember(request, login)
                        return HTTPFound(location=came_from,
                                 headers=headers)
                    break
            message = 'Failed login'

        return {
            'name':'Login',
            'message':message,
            'url':request.application_url + '/login',
            'came_from':came_from,
            'login':login,
            'password':password,
        }

    @view_config(route_name='logout')
    def logout(self):
        request = self.request
        headers = forget(request)
        url = request.route_url('home')
        return HTTPFound(location=url,
                         headers=headers)
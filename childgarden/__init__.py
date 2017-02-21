#! /usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .security import groupfinder

def main(global_config, **settings):
    #Настройки
    authn_policy = AuthTktAuthenticationPolicy('seekrit', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,root_factory='childgarden.models.Root')
    config.include('pyramid_jinja2')
    config.include('pyramid_sqlalchemy')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    #Расписываем маршруты
    config.add_route('home', '/') #если маршрут 127.0.0.1:6543/ то обрабатывается views.py -> def home()
    config.add_route('galery', '/gal') #127.0.0.1:6543/gal => views.py -> def galery()
    config.add_route('spisok', '/spis')
    config.add_route('calendar', '/calendar')
    config.add_route('callback', '/callback')
    config.add_route('addEvent', '/addEvent')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()

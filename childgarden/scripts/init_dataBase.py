# -*- coding: utf-8 -*-
import os
import sys

import transaction
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars
from pyramid_sqlalchemy import BaseObject as Base
from pyramid_sqlalchemy import Session as DBSession
from sqlalchemy import engine_from_config

from ..models import (
    User,
    Group,
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        DBSession.add_all([
             User(UserName='admin', UserPass='admin'),
             User(UserName='user', UserPass='user'),
             Group(GroupName='123', VospName='123'),
        ])
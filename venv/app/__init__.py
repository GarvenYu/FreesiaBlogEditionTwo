#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import configparser
import os

bootstrap = Bootstrap()
db = SQLAlchemy()
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))


def create_app():
    app = Flask(__name__)
    config = configparser.ConfigParser()
    config.read_file(open(CURRENT_PATH + '/resource/defaults.cfg'))
    app.config['SQLALCHEMY_DATABASE_URI'] = config['sqlalchemy']['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['sqlalchemy'].getboolean('SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config['SECRET_KEY'] = config['app']['SECRET_KEY']
    app.config['BLOGS_PER_PAGE'] = config['app'].getint('BLOGS_PER_PAGE')
    app.jinja_env.filters['format_date'] = format_date
    app.jinja_env.filters['format_time'] = format_time
    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app


def format_date(datetime):
    return datetime.strftime('%Y')+'年'+datetime.strftime('%m')+'月'+datetime.strftime('%d')+'日'


def format_time(datetime):
    return datetime.strftime('%H')+':'+datetime.strftime('%M')+':'+datetime.strftime('%S')
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/freesiawebsite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = 'something'
    app.config['BLOGS_PER_PAGE'] = 6
    app.jinja_env.filters['format_date'] = format_date
    app.jinja_env.filters['format_time'] = format_time
    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


def format_date(datetime):
    return datetime.strftime('%Y')+'年'+datetime.strftime('%m')+'月'+datetime.strftime('%d')+'日'


def format_time(datetime):
    return datetime.strftime('%H')+':'+datetime.strftime('%M')+':'+datetime.strftime('%S')
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
    app = Flask('app')
    config = configparser.ConfigParser()
    config.read_file(open(CURRENT_PATH + '/resource/defaults.cfg'))
    # 配置SqlAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = config['SqlAlchemy']['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['SqlAlchemy'].getboolean('SQLALCHEMY_TRACK_MODIFICATIONS')
    # 配置应用
    app.config['SECRET_KEY'] = config['app']['SECRET_KEY']
    app.config['BLOG_PER_PAGE'] = config['app'].getint('BLOG_PER_PAGE')
    # 注册JinJa2过滤器
    app.jinja_env.filters['format_date'] = format_date
    app.jinja_env.filters['format_time'] = format_time

    bootstrap.init_app(app)
    db.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from app.dashboard import manage as manage_blueprint
    app.register_blueprint(manage_blueprint, url_prefix="/manage")

    return app


def format_date(datetime):
    return datetime.strftime('%Y')+'年'+datetime.strftime('%m')+'月'+datetime.strftime('%d')+'日'


def format_time(datetime):
    return datetime.strftime('%H')+':'+datetime.strftime('%M')+':'+datetime.strftime('%S')
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import configparser
import os
from datetime import timedelta

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))


def create_app():
    app = Flask(__name__)
    config = configparser.ConfigParser()
    config.read_file(open(CURRENT_PATH + '/resource/defaults.cfg'))
    # 配置SqlAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = config['SqlAlchemy']['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['SqlAlchemy'].getboolean('SQLALCHEMY_TRACK_MODIFICATIONS')
    # 配置应用
    app.config['SECRET_KEY'] = config['app']['SECRET_KEY']
    app.config['BLOG_PER_PAGE'] = config['app'].getint('BLOG_PER_PAGE')
    # 配置flask_login
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=120)
    # 注册JinJa2过滤器
    app.jinja_env.filters['format_date'] = format_date
    app.jinja_env.filters['format_time'] = format_time
    # 配置flask_login
    login_manager.login_view = "auth.login"
    login_manager.session_protection = "strong"
    login_manager.login_message = "请先登录"
    # 注册到flask中
    login_manager.init_app(app)
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
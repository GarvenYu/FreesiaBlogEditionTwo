#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from app.extensions import bootstrap, db
import configparser
import os
from app.main import main as main_blueprint
from app.auth import auth as auth_blueprint
from app.dashboard import manage as manage_blueprint

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))


def create_app():
    app = Flask('app')
    config = configparser.ConfigParser()
    config.read_file(open(CURRENT_PATH + '/resource/defaults.cfg'))

    register_config(app, config)  # 注册配置
    register_extensions(app)  # 注册扩展
    register_blueprints(app)  # 注册蓝本
    register_filter(app)  # 注册过滤器
    register_error(app)  # 注册错误处理
    return app


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(manage_blueprint, url_prefix="/manage")


def register_config(app, config):
    # 配置SqlAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = config['SqlAlchemy']['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['SqlAlchemy'].getboolean('SQLALCHEMY_TRACK_MODIFICATIONS')
    # 配置应用
    app.config['SECRET_KEY'] = config['app']['SECRET_KEY']
    app.config['BLOG_PER_PAGE'] = config['app'].getint('BLOG_PER_PAGE')


def register_filter(app):
    # 注册JinJa2过滤器
    app.jinja_env.filters['format_date'] = lambda datetime: \
        datetime.strftime('%Y') + '年' + datetime.strftime('%m') + '月' + datetime.strftime('%d') + '日'
    app.jinja_env.filters['format_time'] = lambda datetime: \
        datetime.strftime('%H') + ':' + datetime.strftime('%M') + ':' + datetime.strftime('%S')


def register_error(app):
    @app.errorhandler(404)
    def page_not_found(exception):
        return render_template('error/404.html'), 404
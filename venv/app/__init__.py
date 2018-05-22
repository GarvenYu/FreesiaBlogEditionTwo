#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/freesiawebsite'

    Bootstrap(app)
    db = SQLAlchemy(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
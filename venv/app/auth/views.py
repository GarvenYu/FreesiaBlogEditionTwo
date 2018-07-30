#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import auth
from flask import render_template


@auth.route('/login', methods=['GET'])
def login():
    """登录"""
    return render_template('user/login.html')
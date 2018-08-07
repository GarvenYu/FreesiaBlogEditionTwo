#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import auth
from flask import render_template, request, redirect, url_for, flash
from ..models import User


@auth.route('/login', methods=['GET'])
def login():
    """登录"""
    return render_template('user/login.html')


@auth.route('/authLogin', methods=['POST'])
def auth_login():
    """验证登录"""
    email = request.form.get('inputEmail', None)
    password = request.form.get('inputPassword', None)
    remember = request.form.get('remember_me', None)
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        return redirect(url_for('main.index'))
    else:
        flash("账号或密码错误!")
        return redirect(url_for('auth.login'))
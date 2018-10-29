#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import auth
from flask import render_template, request, redirect, url_for, flash, make_response
from flask_login import login_user
from app.models import User, Role
from app.utils import add_token
import json


@auth.route('/login', methods=['GET'])
def login():
    """登录"""
    return render_template('user/login.html')


@auth.route('/authLogin', methods=['POST'])
def auth_login():
    """验证登录"""
    email = request.form.get('inputEmail', None)
    password = request.form.get('inputPassword', None)
    remember = True if request.form.get('remember_me', None) else False
    user = User.query.filter_by(email=email).first()
    # 获取权限
    role = Role.query.filter_by(id=user.role_id).first().role_cd
    if user and user.verify_password(password):
        # 存储用户信息
        user_info = {
            "id": user.id,
            "email": user.email,
            "role": role
        }
        token = add_token(user_info)
        # 发送cookie
        resp = make_response(redirect(request.args.get('next') or url_for('main.index')))
        resp.set_cookie('token', value=token, max_age=86400)
        return resp
    else:
        flash("账号或密码错误!")
        return redirect(url_for('auth.login'))
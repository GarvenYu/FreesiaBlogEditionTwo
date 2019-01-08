#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app.auth import auth
from flask import render_template, request, redirect, url_for, flash, make_response
from app.models import User, Role
from app.utils import add_token


@auth.route('/login', methods=['GET'])
def login():
    """登录"""
    nexturl = request.args.get('next', url_for('main.index'))
    return render_template('user/login.html', nexturl=nexturl)


@auth.route('/authLogin', methods=['POST'])
def auth_login():
    """验证登录"""
    email = request.form.get('inputEmail', None)
    password = request.form.get('inputPassword', None)
    remember = True if request.form.get('remember_me', None) else False
    nexturl = request.form.get('nexturl')  # 默认主页
    user = User.query.filter_by(email=email).first()  # 加载用户
    if user and user.verify_password(password):
        # 是否已有token
        token = request.cookies.get('token')
        if not token:
            # 存储用户信息
            user_info = {
                "id": user.id,
                "email": user.email,
                "role": user.role.role_cd
            }
            # add token and user_info to redis hash
            token = add_token(user_info)
            # send cookie to client
            resp = make_response(redirect(nexturl))
            resp.set_cookie('token', value=token, max_age=86400)
            return resp
        else:
            # 视为已登录
            return redirect(nexturl)
    else:
        flash("账号或密码错误!")
        return redirect(url_for('auth.login'))

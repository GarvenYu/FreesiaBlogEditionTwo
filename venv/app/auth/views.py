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
    email = request.form['inputEmail']
    password = request.form['inputPassword']
    remember = request.form['remember_me']
    user = User.query.filter_by(email=email).first()
    if not user and user.verify_password(password):
        return redirect(url_for('main.index'))
    flash("Invalid Data")
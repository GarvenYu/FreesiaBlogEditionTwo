#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import conn
import functools
from flask import g
import uuid
import json

TOKEN_KEY = 'user:token:'


def check_token(token):
    """根据token加载用户"""
    return conn.hget(TOKEN_KEY, token)


def add_token(user_info):
    """添加用户token"""
    token = str(uuid.uuid3(uuid.NAMESPACE_DNS, user_info.get('email')))
    conn.hset(TOKEN_KEY, token, json.dumps(user_info))
    return token


def check_auth(request):
    """装饰器，获取客户端cookie信息检查用户权限"""
    def wrapper(func):
        @functools.wraps(func)
        def call(*args, **kwargs):
            # 获取客户端token
            token = request.cookies.get('token')
            user_info = check_token(token)
            g.user = user_info
            if not user_info:
                g.have_auth = False
            else:
                user = json.loads(user_info)
                g.have_auth = True if user.get('role') == "admin" else False
            return func(*args, **kwargs)
        return call
    return wrapper
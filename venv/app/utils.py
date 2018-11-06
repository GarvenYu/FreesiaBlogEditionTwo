#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
from flask import g
import uuid
import json
import redis


TOKEN_KEY = 'user:token:'
conn = redis.Redis(host="localhost", port=6379, decode_responses=True)


def load_user(token):
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
            user_info = load_user(token)
            g.user = user_info
            if not user_info:
                g.have_auth = False
            else:
                user = json.loads(user_info)
                g.have_auth = True if user.get('role') == "admin" else False
            return func(*args, **kwargs)
        return call
    return wrapper
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""工具类
@author: ykbpro@whut.edu.cn
@time: 2018-11-11 20:29:30
"""

import functools
from flask import g
import uuid
import json
import redis
from app import db
from app.models import Category, Blog, Message, MessageEncoder, ReplyComment, ReplyEncoder, Role
from sqlalchemy import func as f, asc, desc


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


def load_bas_info(request):
    """处理请求前预加载信息
    :param request: flask.request
    :return: g
    """
    def wrapper(func):
        @functools.wraps(func)
        def call(*args, **kwargs):
            # 加载用户
            token = request.cookies.get('token')
            user = json.loads(load_user(token)) if token and type(load_user(token)) is str else None
            g.user = user
            # 侧边栏博客分类
            kind_number = db.session.query(Category.name, Category.id, f.count(Blog.category_id)) \
                .join(Blog, Blog.category_id == Category.id).group_by(Category.name, Category.id).all()
            g.kindnumber = kind_number
            return func(*args, **kwargs)
        return call
    return wrapper
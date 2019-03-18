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
import os
import configparser
from app.extensions import db
from app.models import Category, Blog
from sqlalchemy import func as f

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read_file(open(CURRENT_PATH + '/resource/defaults.cfg'))
TOKEN_KEY = config['redis']['TOKEN_KEY']
HOT_WORDS_ZSET = config['redis']['HOT_WORDS_ZSET']
HOT_WORDS_NUMBERS = config['redis'].getint('WORDS_COUNTS')
conn = redis.Redis(host="localhost", port=6379, decode_responses=True)
conn2 = redis.Redis(db=1, decode_responses=True)


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


def autocomplete_words() -> list:
    """
    返回搜索高频词汇有序集合中所有成员
    :return: list
    """
    return conn.zrevrange(HOT_WORDS_ZSET, 0, -1)


def handle_search_words(word):
    """
    搜索词增加搜索次数
    :param word: 搜索词
    :return: 
    """
    pipeline = conn.pipeline(True)
    while 1:
        try:
            exist = conn.zrank(HOT_WORDS_ZSET, word)
            current_words_counts = conn.zcard(HOT_WORDS_ZSET)
            pipeline.watch(HOT_WORDS_ZSET)
            if exist is not None:
                # 如果搜索词已存在
                # 增加搜索次数
                pipeline.zincrby(HOT_WORDS_ZSET, 1, word)
            elif current_words_counts > HOT_WORDS_NUMBERS:
                # 如果有序集合中的关键字个数超过了设置上限
                # 移除次数最低的元素
                pipeline.zremrangebyrank(HOT_WORDS_ZSET, 0, 0)
                # 添加新的元素
                pipeline.zadd(HOT_WORDS_ZSET, {word: 1})
            else:
                pipeline.zadd(HOT_WORDS_ZSET, {word: 1})
            pipeline.execute()
            break
        except redis.exceptions.WatchError:
            continue


def get_aside_sentence():
    """侧边栏每日一句"""
    keys = conn2.keys()
    if keys:
        try:
            result = conn2.get(keys[0])
            celery_dict = json.loads(result)
            iciba_dict = json.loads(celery_dict.get('result', None))
            if iciba_dict:
                return iciba_dict['content'], iciba_dict['pic']
        except Exception as e:
            raise e

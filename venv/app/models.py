#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import db, login_manager
from flask_login import UserMixin


class Blog(db.Model):
    """博客model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    summary = db.Column(db.Text)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))  # 博客分类
    category = db.relationship('Category', backref=db.backref('blogs', lazy='dynamic'))

    def __init__(self, title, summary, content, time, category):
        self.title = title
        self.summary = summary
        self.content = content
        self.timestamp = time
        self.category = category

    def __repr__(self):
        return '<Blog %r>' % self.title


class Category(db.Model):
    """博客种类model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


class User(db.Model, UserMixin):
    """用户model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email=None, password_hash=None):
        self.email = email
        self.password_hash = password_hash

    def verify_password(self, password):
        return self.password_hash == password


class Message(db.Model):
    """留言model"""
    __tablename__ = "bbs_bas_inf"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    msg_content = db.Column(db.Text)
    msg_time = db.Column(db.DateTime)
    del_ind = db.Column(db.Integer, default=0)
    replies = db.relationship("ReplyComment", backref="message", order_by="ReplyComment.reply_time")

    def __init__(self, user_name, msg_content, msg_time):
        self.user_name = user_name
        self.msg_content = msg_content
        self.msg_time = msg_time


class ReplyComment(db.Model):
    """回复model"""
    __tablename__ = "reply_bas_inf"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50))
    reply_content = db.Column(db.Text)
    reply_time = db.Column(db.DateTime)
    message_id = db.Column(db.Integer, db.ForeignKey("bbs_bas_inf.id"), nullable=False)
    del_ind = db.Column(db.Integer, default=0)

    def __init__(self, user_name, reply_content, reply_time, message_id):
        self.user_name = user_name
        self.reply_content = reply_content
        self.reply_time = reply_time
        self.message_id = message_id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import db
from datetime import datetime


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.String(20))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))  # 博客分类
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, content, tag):
        self.content = content
        self.tag = tag

    def __repr__(self):
        return '<Blog %r>' % self.tag


class Category(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name
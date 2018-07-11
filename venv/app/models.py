#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import db


class Blog(db.Model):
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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<Category %r>' % self.name
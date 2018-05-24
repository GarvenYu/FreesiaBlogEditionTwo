#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import db
from datetime import datetime


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    tag = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())

    def __init__(self, content, tag):
        self.content = content
        self.tag = tag

    def __repr__(self):
        return '<Blog %r>' % self.tag
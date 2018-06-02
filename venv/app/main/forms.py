#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField


class BlogForm(FlaskForm):
    pagedown = PageDownField('Enter your markdown')
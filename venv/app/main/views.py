#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, session, redirect, url_for, request, jsonify
import json
import logging
from . import main
from ..models import Category


logger = logging.getLogger()


@main.route('/mainPage', methods=['GET'])
def index():
    name = session.get('name')
    return render_template('home/mainPage.html', name=name)


@main.route('/write', methods=['GET', 'POST'])
def write_blog():
    categories = Category.query.all()
    option_list = [dict(id=category.id, name=category.name) for category in categories]
    return render_template('blog/write_blog.html', option_list=option_list)


@main.route('/saveBlog', methods=['POST'])
def save_blog():
    data = request.get_data()
    dict_data = json.loads(data)
    # {'blog_title': '得到', 'blog_summary': '对对对', 'states': ['AL', 'WY'], 'content': ''}

    return render_template('home/mainPage.html')
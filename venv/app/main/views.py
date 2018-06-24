#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, session, redirect, url_for, request, jsonify,current_app
import json
import logging
from datetime import datetime
from . import main
from ..models import Category, Blog
from .. import db


logger = logging.getLogger()


@main.route('/mainPage', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Blog.query.order_by(Blog.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLOGS_PER_PAGE'], error_out=False)
    items = pagination.items
    return render_template('home/mainPage.html', items=items, pagination=pagination)


@main.route('/write', methods=['GET', 'POST'])
def write_blog():
    categories = Category.query.all()
    option_list = [dict(id=category.id, name=category.name) for category in categories]
    return render_template('blog/write_blog.html', option_list=option_list)


@main.route('/saveBlog', methods=['POST'])
def save_blog():
    data = request.get_data()
    blog_data = json.loads(data)
    category = Category.query.filter_by(id=int(blog_data['states'][0])).first()
    blog = Blog(blog_data['blog_title'], blog_data['blog_summary'], blog_data['content'], datetime.now(), category)
    db.session.add(blog)
    db.session.commit()
    return jsonify(msg='success')
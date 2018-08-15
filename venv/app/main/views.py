#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify, current_app
import json
import logging
from datetime import datetime
from . import main
from ..models import Category, Blog, Message
from .. import db
import markdown
from sqlalchemy import func
from flask_login import login_required


logger = logging.getLogger()

    
@main.route('/mainPage', methods=['GET'])
def index():
    """获取首页数据"""
    page = request.args.get('page', 1, type=int)
    pagination = Blog.query.order_by(Blog.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLOG_PER_PAGE'], error_out=False)
    items = pagination.items
    kind_number = db.session.query(Category.name, Category.id, func.count(Blog.category_id)) \
        .join(Blog, Blog.category_id == Category.id).group_by(Category.name, Category.id).all()
    side_items = Blog.query.order_by(Blog.timestamp.desc()).limit(6).offset(0).all()  # 侧边栏最近文章
    return render_template('home/mainPage.html', items=items, sideitems=side_items,
                           pagination=pagination, kindnumber=kind_number, mainPage=True)


@main.route('/write', methods=['GET', 'POST'])
@login_required
def write_blog():
    """编辑博客"""
    categories = Category.query.all()
    option_list = [dict(id=category.id, name=category.name)
                   for category in categories]
    return render_template('blog/write_blog.html', option_list=option_list)


@main.route('/saveBlog', methods=['POST'])
def save_blog():
    """存储博客"""
    data = request.get_data()
    blog_data = json.loads(data)
    category = Category.query.filter_by(id=int(blog_data['states'][0])).first()
    blog = Blog(blog_data['blog_title'], blog_data['blog_summary'],
                blog_data['content'], datetime.now(), category)
    db.session.add(blog)
    db.session.commit()
    return jsonify(msg='success')


@main.route('/detail/<int:id>', methods=['GET'])
def check_blog(id):
    """获取博客详情"""
    blog = Blog.query.filter_by(id=id).first()
    blog.content = markdown.markdown(blog.content)
    kind_number = db.session.query(Category.name, Category.id, func.count(Blog.category_id)) \
        .join(Blog, Blog.category_id == Category.id).group_by(Category.name, Category.id).all()
    return render_template('blog/blog_detail.html', blog=blog, kindnumber=kind_number)


@main.route('/blogkind', methods=['GET'])
def get_blog_by_kind():
    """获取分类下所有博客"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category_id', type=int)
    pagination = Blog.query.filter_by(category_id=category_id).order_by(Blog.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLOG_PER_PAGE'], error_out=False)
    items = pagination.items
    kind_number = db.session.query(Category.name, Category.id, func.count(Blog.category_id)) \
        .join(Blog, Blog.category_id == Category.id).group_by(Category.name, Category.id).all()
    side_items = Blog.query.order_by(Blog.timestamp.desc()).limit(6).offset(0).all()  # 侧边栏最近文章
    return render_template('home/mainPage.html', items=items, sideitems=side_items,
                           pagination=pagination, kindnumber=kind_number, category_id=category_id, mainPage=False)


@main.route('/message', methods=['GET'])
def show_message():
    return render_template('blog/message_board.html')


@main.route('/saveMessage', methods=['POST'])
def save_message():
    """保存留言"""
    message_data = json.loads(request.get_data())
    if not message_data['user_name'] or not message_data['message_content']:
        pass
    else:
        message = Message(message_data['user_name'], message_data['message_content'], datetime.now())
        db.session.add(message)
        db.session.commit()
        return jsonify(msg='success')
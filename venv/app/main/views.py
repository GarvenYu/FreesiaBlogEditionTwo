#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify, current_app, redirect, url_for, make_response
import json
import logging
from datetime import datetime
from . import main
from ..models import Category, Blog, Message, MessageEncoder, ReplyComment, ReplyEncoder
from .. import db
import markdown
from sqlalchemy import func, asc, desc
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
    """加载留言板页面"""
    kind_number = db.session.query(Category.name, Category.id, func.count(Blog.category_id)) \
        .join(Blog, Blog.category_id == Category.id).group_by(Category.name, Category.id).all()
    response = make_response(render_template('blog/message_board.html', kindnumber=kind_number))
    return response


@main.route('/getMessage', methods=['POST'])
def get_message():
    """获取留言板数据"""
    result_list = []  # 封装评论和回复
    message_list = Message.query.filter_by(del_ind=0).order_by(desc(Message.msg_time)).all()
    reply_list = ReplyComment.query.filter_by(del_ind=0).order_by(asc(ReplyComment.message_id),
                                                                  desc(ReplyComment.reply_time)).all()
    # result_list.append(json.dumps(message_list, cls=MessageEncoder))
    # result_list.append(json.dumps(reply_list, cls=ReplyEncoder))
    return json.dumps(message_list, cls=MessageEncoder)


@main.route('/saveMessage', methods=['POST'])
def save_message():
    """保存留言"""
    message_data = json.loads(request.get_data())
    if not message_data['user_name'] or not message_data['message_content']:
        pass
    else:
        """存储留言"""
        message = Message(message_data['user_name'], message_data['message_content'], datetime.now())
        db.session.add(message)
        db.session.commit()
        """加载留言"""
        message_list = Message.query.order_by(Message.msg_time.desc()).all()
        return jsonify(messages=message_list)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 2018-11-13 23:32:05
# ykbpro@whut.edu.cn
# 博客后台功能管理

from app.dashboard import manage
from app.utils import load_bas_info
from flask import render_template, request, redirect, url_for, g
from app.models import Blog, Category
from app import db


@manage.route('/dashboard', methods=['GET'])
@load_bas_info(request)
def show_dash_board():
    """进入后台管理
    """
    # 已登录
    if g.user:
        # 管理员权限
        g.have_auth = True if g.user.get('role') == "admin" else False
        if g.have_auth:
            blogs = Blog.query.order_by(Blog.timestamp.desc()).all()
            return render_template('blog/dashboard.html', blogs=blogs)
        else:
            # 游客权限
            return redirect(url_for('main.index'))
    # 未登录
    return redirect(url_for('auth.login', next=request.path))


@manage.route('/deleteblog', methods=['POST'])
def delete_blog():
    """删除博客
    """
    blog_id = request.args.get('id')
    blog = Blog.query.get(blog_id)
    if blog:
        db.session.delete(blog)
        db.session.commit()
    return redirect(url_for('manage.show_dash_board'))


@manage.route('/updateblog', methods=['POST'])
@load_bas_info(request)
def update_blog():
    """更新博客
    """
    blog = Blog.query.get(request.form.get('id'))
    if blog:
        categories = Category.query.all()
        option_list = [dict(id=category.id, name=category.name)
                       for category in categories]
        return render_template('blog/update_blog.html', blog=blog, option_list=option_list)
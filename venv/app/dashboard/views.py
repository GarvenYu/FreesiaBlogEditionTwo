#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 2018-11-13 23:32:05
# ykbpro@whut.edu.cn
# 博客后台功能管理

from app.dashboard import manage
from app.utils import load_bas_info
from flask import render_template, request, redirect, url_for, g


@manage.route('/dashboard', methods=['GET'])
@load_bas_info(request)
def showdashboard():
    """进入后台管理
    """
    # 已登录
    if g.user:
        # 管理员权限
        g.have_auth = True if g.user.get('role') == "admin" else False
        if g.have_auth:
            return render_template('blog/dashboard.html')
        else:
            # 游客权限
            return redirect(url_for('main.index'))
    # 未登录
    return redirect(url_for('auth.login', next=request.path))
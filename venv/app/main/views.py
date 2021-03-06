#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify, current_app, g, redirect, url_for, make_response
import json
import os
import logging
import socket
import configparser
from datetime import datetime
from app.main import main
from app.models import Category, Blog, Message, MessageEncoder, ReplyComment
from app.extensions import db
import markdown
from sqlalchemy import desc, or_, func
from app.utils import load_bas_info, autocomplete_words, handle_search_words, get_aside_sentence

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
RESOURCE_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), '../..')) + '/resource/defaults.cfg'


@main.route('/', methods=['GET'])
@load_bas_info(request)
def index():
    """获取首页数据
    """
    page = request.args.get('page', 1, type=int)
    pagination = Blog.query.order_by(Blog.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLOG_PER_PAGE'], error_out=False)
    items = pagination.items
    # 侧边栏最近文章
    side_items = Blog.query.order_by(Blog.timestamp.desc()).limit(6).offset(0).all()
    # 侧边栏最近留言
    recent_comments = Message.query.filter_by(del_ind=0) \
        .order_by(Message.msg_time.desc()).limit(5).offset(0).all()
    return render_template('home/mainPage.html', items=items, sideitems=side_items, iciba=get_aside_sentence(),
                           pagination=pagination, recentComments=recent_comments, mainPage=True)


@main.route('/write', methods=['GET'])
@load_bas_info(request)
def write_blog():
    """编辑博客
    """
    # 已登录
    if g.user:
        # 管理员权限
        g.have_auth = True if g.user.get('role') == "admin" else False
        if g.have_auth:
            categories = Category.query.all()
            option_list = [dict(id=category.id, name=category.name)
                           for category in categories]
            return render_template('blog/write_blog.html', option_list=option_list)
        else:
            # 游客权限
            return redirect(url_for('main.index'))
    # 未登录
    return redirect(url_for('auth.login', next=request.path))


@main.route('/saveBlog', methods=['POST'])
def save_blog():
    """存储博客
    """
    data = request.get_data()
    blog_data = json.loads(data)
    category = Category.query.filter_by(id=int(blog_data['states'][0])).first()
    blog = Blog(blog_data['blog_title'], blog_data['blog_summary'],
                blog_data['content'], datetime.now(), category)
    db.session.add(blog)
    db.session.commit()
    return jsonify(msg='success')


@main.route('/updateBlogInfo', methods=['POST'])
def update_blog_info():
    """更新博客
    """
    blog_data = request.get_json()
    category = Category.query.filter_by(id=int(blog_data['states'][0])).first()
    blog = Blog.query.get(blog_data.get('id', None))
    if blog:
        blog.title = blog_data.get('blog_title')
        blog.summary = blog_data.get('blog_summary')
        blog.content = blog_data.get('content')
        blog.category = category
    db.session.commit()
    return jsonify(msg='success')


@main.route('/detail/<int:id>', methods=['GET'])
@load_bas_info(request)
def check_blog(id: int):
    """获取博客详情
    """
    blog = Blog.query.get_or_404(id)
    blog.content = markdown.markdown(blog.content)
    return render_template('blog/blog_detail.html', blog=blog)


@main.route('/blogkind', methods=['GET'])
@load_bas_info(request)
def get_blog_by_kind():
    """获取分类下所有博客
    """
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category_id', type=int)
    pagination = Blog.query.filter_by(category_id=category_id).order_by(Blog.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLOG_PER_PAGE'], error_out=False)
    items = pagination.items
    # 侧边栏最近文章
    side_items = Blog.query.order_by(Blog.timestamp.desc()).limit(6).offset(0).all()
    return render_template('home/mainPage.html', items=items, sideitems=side_items,
                           pagination=pagination, category_id=category_id, mainPage=False)


@main.route('/message', methods=['GET'])
@load_bas_info(request)
def show_message():
    """加载留言板页面
    """
    response = make_response(render_template('blog/message_board.html'))
    return response


@main.route('/getMessage', methods=['GET'])
def get_message():
    """获取留言板数据
    """
    message_list = Message.query.filter_by(del_ind=0).order_by(desc(Message.msg_time)).all()
    return json.dumps(message_list, cls=MessageEncoder)


@main.route('/saveMessage', methods=['POST'])
def save_message():
    """存储留言
    """
    message = Message(request.form.get('user_name'), request.form.get('message_content'), datetime.now())
    db.session.add(message)
    db.session.commit()
    return jsonify(message="评论成功")


@main.route('/saveReply', methods=['POST'])
def save_reply():
    """存储回复
    """
    reply = ReplyComment(request.form.get('user_name'), request.form.get('reply_content'), datetime.now(),
                         request.form.get('message_id'))
    db.session.add(reply)
    db.session.commit()
    return jsonify(message="回复成功")


def check_extension(file_name: str) -> bool:
    """检查文件扩展名
    """
    return '.' in file_name and file_name.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/savePicture', methods=['POST'])
def save_picture():
    """存储图片
    """
    if request.method == 'POST':
        file = request.files['file']
        if check_extension(file.filename):
            config = configparser.ConfigParser()
            config.read_file(open(RESOURCE_PATH))
            client_socket = socket.socket()
            client_socket.connect((config['app']['IP'], config['app'].getint('PORT')))
            file_size = request.content_length
            # client_socket.send(str(file_size).encode('utf-8'))
            # logger.info("发送文件长度.. %d" % request.content_length)
            send_size = 0
            while send_size <= request.content_length:
                if file_size - send_size > 4096:
                    # logger.info("发送文件.. %d" % send_size)
                    client_socket.send(file.read(4096))
                else:
                    # logger.info("发送文件.. %d" % send_size)
                    client_socket.send(file.read(file_size - send_size))
                send_size += 4096
            logger.info("发送文件.. %d" % send_size)
            # client_socket.send("finish".encode('utf-8'))
            picture_url = client_socket.recv(4096)
            logger.info("接收服务器返回地址.. %s" % picture_url.decode('UTF-8'))
            if picture_url:
                client_socket.close()
                return jsonify(url=picture_url.decode('UTF-8'))
            logger.info("未接收到返回数据...")
        return jsonify(url='未接收到返回数据...')


@main.route('/autocomplete', methods=['GET'])
def autocomplete_search_info() -> json:
    """
    补全搜索信息
    :return: json
    """
    words = autocomplete_words()
    prefix = request.args.get('key')
    results = []
    for word in words:
        if word.lower().startswith(prefix):
            results.append(word)
    return jsonify(data=results)


@main.route('/search', methods=['POST'])
def search():
    """
    主页搜索，完成两项工作，1.redis中处理搜索词 2.返回搜索结果
    :return:
    """
    word = request.form.get('searchInput')
    handle_search_words(word)
    search_results = Blog.query.filter(
        or_(Blog.title.like('%%%s%%' % word), Blog.summary.like('%%%s%%' % word))).order_by(
        Blog.timestamp.desc()).all()
    final_results = []
    if search_results:
        searched = True
        # 根据年份将搜索结果进行分组
        # 初始化final_results
        max_year = search_results[0].timestamp.year
        count = 0
        for blog in search_results:
            if blog.timestamp.year == max_year:
                count += 1
            else:
                final_results.append([1] * count)
                max_year = blog.timestamp.year
                count = 1
        final_results.append([1] * count)
        # 填入数据
        # 每一年的结果存在同一个列表中
        index = 0
        for i in range(len(final_results)):
            for j in range(len(final_results[i])):
                if final_results[i][j]:
                    final_results[i][j] = search_results[index]
                    index += 1
    else:
        searched = False
        # 随机选取博客进行展示
        final_results = Blog.query.order_by(func.rand()).limit(5).all()
    return render_template('blog/search_results.html', results=final_results, searched=searched)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, session, redirect, url_for, request
from . import main
from .forms import BlogForm


@main.route('/mainPage', methods=['GET'])
def index():
    name = session.get('name')
    return render_template('home/mainPage.html', name=name)


@main.route('/write', methods=['GET', 'POST'])
def write_blog():
    return render_template('blog/write_blog.html')


@main.route('/saveBlog', methods=['POST'])
def save_blog():
    title = request.form['blog_title']
    summary = request.form['blog_summary']
    tag = request.form['states[]']
    content = request.form['content']
    return render_template('home/mainPage.html', title=title, summary=summary, tag=tag, content=content)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, session, redirect, url_for
from . import main
from .forms import BlogForm


@main.route('/mainPage', methods=['GET'])
def index():
    name = session.get('name')
    return render_template('home/mainPage.html', name=name)


@main.route('/write', methods=['GET', 'POST'])
def write_blog():
    form = BlogForm()
    if form.validate_on_submit():
        text = form.pagedown.data
        session['name'] = form.name.data
        return redirect(url_for(".index"))
    return render_template('blog/write_blog.html', form=form)
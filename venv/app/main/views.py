#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template
from . import main


@main.route('/', methods=['GET'])
def index():
    return render_template('base.html', info='test')
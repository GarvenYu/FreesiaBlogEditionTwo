#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    return render_template('base.html', info='test')


@app.route('/user/<name>')
def hello(name):
    return render_template('user.html', name=name)


@app.route('/user/<int:id>')
def hello_id(id):
    return '<h1>hello id is %05d!</h1>' % id


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)
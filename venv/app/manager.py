#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import create_app
from gevent.pywsgi import WSGIServer



app = create_app()
server = WSGIServer(('127.0.0.1', 8000), app)
server.serve_forever()
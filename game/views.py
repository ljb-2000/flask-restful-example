# -*- coding:utf-8 -*-
'''
Created on 2015年6月22日

@author: nob
'''
from flask import Blueprint, request
from .extensions import db
from .models import User

home = Blueprint('home', __name__, static_url_path="/static", template_folder='templates', static_folder='static')


@home.route('/create_db')
def create_db():
    from .models import (User, Task)
    db.create_all()
    return u"create tables ok!"

@home.route('/')
def index():
    return "hello,welcome to bet app!"

@home.route('/arg')
def argtest():
    token = request.args.get('x')
    user = User.verify_auth_token(token)
    return "argtest"
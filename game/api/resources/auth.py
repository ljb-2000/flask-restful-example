# -*- coding:utf-8 -*-
'''
Created on 2015年6月22日

@author: nob
'''
from functools import wraps
from flask import request, g
from flask.ext.restful import abort
from ...models import User
from ..constants import AUTH_HEADER_NAME, TOKEN_EXPIRES_IN

def requires_auth_token(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get(AUTH_HEADER_NAME)
        if not token:
            abort(401, message=u"未授权用户")
        user = User.verify_auth_token(token)
        if not user:
            abort(401, message=u"Token验证错误或者已过期")
        g.user = user
        return func(*args, **kwargs)
    return decorated

def login_as(user):
    user.generate_auth_token(TOKEN_EXPIRES_IN)
    g.user = user
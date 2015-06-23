# -*- coding:utf-8 -*-
'''
Created on 2015年6月22日

@author: nob
'''
from functools import wraps
from flask import abort, request, g
from ...models import User

def requires_auth_token(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.pop('X-Server-Auth-Token')
        user = User.verify_auth_token(token)
        if not user:
            abort(401)
        g.user = user
        return func(*args, **kwargs)
    return decorated

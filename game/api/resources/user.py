# -*- coding:utf-8 -*-
'''
Created on 2015年6月22日

@author: nob
'''
from flask import abort, g
from flask.ext.restful import Resource, reqparse, marshal_with, fields
from ...models import User
from .. import api
from .auth import requires_auth_token

login_parser = reqparse.RequestParser()
login_parser.add_argument('phone', type=str, required=True, help="phone cannot be blank!")
login_parser.add_argument('password', type=str, required=True, help="password cannot be blank!")

user_parser = reqparse.RequestParser()
user_parser.add_argument('phone', type=str, required=True, help="phone cannot be blank!")
user_parser.add_argument('nickname', type=str)
user_parser.add_argument('password', type=str)

# From the request headers
# parser.add_argument('User-Agent', type=str, location='headers')

# Marshaled field definitions for user objects
user_fields = {
    'id': fields.Integer,
    'phone': fields.String,
    'nickname': fields.String,
    'token':fields.String(attribute='token', default=''),
}

# Marshaled field definitions for list of user objects
user_list_fields = {
    'id': fields.Integer,
    'phone': fields.String,
    'nickname': fields.String,
}

@api.resource('/login')
class Login(Resource):
    @marshal_with(user_fields)
    def get(self):
        args = login_parser.parse_args()
        user = User.get_by_phone(args.get('phone', None))
        if not user:
            return {'message':u'用户不存在'}, 401
        if not user.verify_password(args.get('password', None)):
            return {'message':u'密码错误'}, 401
        user.generate_auth_token(86400*30)
        g.user = user
        return user, 200

@api.resource('/users')
class UserListRes(Resource):
    @marshal_with(user_list_fields)
    def get(self):
        users = User.query.all()
        return users

    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        user = User.create(**args)
        return user, 201, {'Location': api.url_for(UserRes, id = user.id, _external = True, _method='GET')}

@api.resource('/users/<int:id>', '/users/<phone>', endpoint='api.get_user')
class UserRes(Resource):
    @marshal_with(user_fields)
    def get(self, id=0, phone=None):
        user = None
        if phone:
            user = User.get_by_phone(phone)
        elif id:
            user = User.get_by_id(id)
        if not user:
            abort(404)
        return user

    @requires_auth_token
    @marshal_with(user_fields)
    def put(self, user_id=0, username=None):
        g.user.update(**user_parser.parse_args())
        return g.user

    @requires_auth_token
    def delete(self, user_id=0, username=None):
        g.user.delete()
        return 204
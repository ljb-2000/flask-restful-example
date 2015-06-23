# -*- coding:utf-8 -*-
'''
Created on 2015年6月22日

@author: nob
'''
from flask import g
from flask.ext.restful import Resource, reqparse, marshal_with, fields, abort
from ...models import User
from .. import api
from .auth import requires_auth_token, login_as

login_parser = reqparse.RequestParser()
login_parser.add_argument('phone', type=str, location='args', required=True, help="phone cannot be blank!")
login_parser.add_argument('password', type=str, location='args', required=True, help="password cannot be blank!")

user_parser = reqparse.RequestParser()
user_parser.add_argument('phone', type=str, required=True, help="phone cannot be blank!")
user_parser.add_argument('nickname', type=str, required=True)
user_parser.add_argument('password', type=str, required=True)

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
def abort_if_user_doesnt_exist(userid):
    user = User.get_by_id(userid)
    if user is None:
        abort(404, message="User {} doesn't exist".format(userid))
    return user

@api.resource('/login')
class LoginResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        args = login_parser.parse_args()
        phone = args.get('phone')
        user = User.get_by_phone(phone)

        if user is None:
            abort(401, message="User doesn't exist for phone {}".format(phone))
        if not user.verify_password(args.get('password', None)):
            abort(401, message="User's password is error for phone {} ".format(phone))

        login_as(user)
        return g.user, 200

@api.resource('/users', endpoint='users')
class UserListResource(Resource):
    @marshal_with(user_list_fields)
    def get(self):
        users = User.query.all()
        return users

    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        phone = args.get('phone')
        if User.get_by_phone(phone):
            abort(409, message="A user with that phone {} already exists.".format(phone))

        user = User.create(**args)
        login_as(user)
        return g.user, 201, {'Location': api.url_for(UserResource, id = user.id, _external = True, _method='GET')}

@api.resource('/users/<int:userid>', endpoint='user')
class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, userid=0):
        return abort_if_user_doesnt_exist(userid)

    @requires_auth_token
    @marshal_with(user_fields)
    def put(self, userid=0):
        # 重写输入参数
        user_parser.replace_argument('phone', type=str)
        user_parser.replace_argument('nickname', type=str)
        user_parser.replace_argument('password', type=str)
        if userid == g.user.id:
            g.user.update(**user_parser.parse_args())
            return g.user, 201
        else:
            abort(403, message=u"只能修改自己的资料")

    @requires_auth_token
    def delete(self, user_id=0, username=None):
        g.user.delete()
        return 204
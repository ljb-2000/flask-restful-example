# -*- coding:utf-8 -*-
'''
Created on 2015年6月23日

@author: nob
'''
from flask import abort
from flask.ext.restful import Resource, reqparse, marshal_with, fields

from ...models import Task, User
from ...helpers import paginate
from .. import meta_fields
from .auth import requires_auth_token


task_parser = reqparse.RequestParser()
task_parser.add_argument('complete', type=bool)
task_parser.add_argument('summary', type=str, required=True)
task_parser.add_argument('description', type=str)

task_list_parser = reqparse.RequestParser()
task_list_parser.add_argument('complete', type=int)


# Marshaled field definitions for task objects
task_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'complete': fields.Boolean,
    'summary': fields.String,
    'description': fields.String,
}

# Marshaled field definitions for collections of task objects
task_list_fields = {
    'items': fields.List(fields.Nested(task_fields)),
    'meta': fields.Nested(meta_fields),
}


class TaskResource(Resource):
    decorators = [
        requires_auth_token,
    ]

    @marshal_with(task_fields)
    def get(self, task_id=0, **kwargs):
        task = Task.get_by_id(task_id)

        if not task:
            abort(404)

        return task

    @marshal_with(task_fields)
    def post(self, task_id=0, **kwargs):
        task = Task.get_by_id(task_id)

        if not task:
            abort(404)

        task.update(**task_parser.parse_args())
        return task

    def delete(self, task_id=0, **kwargs):
        task = Task.get_by_id(task_id)

        if not task:
            abort(404)

        task.delete()
        return 204


class TaskListResource(Resource):
    decorators = [
        requires_auth_token,
    ]

    @marshal_with(task_list_fields)
    @paginate()
    def get(self, user_id=0, phone=''):
        # Find user that task goes with
        if user_id:
            user = User.get_by_id(user_id)
        elif phone:
            user = User.get_by_phone(phone)

        if not user:
            abort(404)

        # Get the user's tasks
        tasks = Task.query.filter_by(user_id=user.id)

        args = task_list_parser.parse_args()
        # fancy url argument query filtering!
        if args['complete'] is not None:
            tasks.filter_by(complete=args['complete'])

        return tasks

    @marshal_with(task_fields)
    def post(self, user_id=0, username=''):
        args = task_parser.parse_args()
        # user owns the task
        args['user_id'] = user_id
        task = Task.create(**args)
        return task, 201

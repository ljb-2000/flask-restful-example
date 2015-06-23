# -*- coding:utf-8 -*-
from flask import Flask, Blueprint, current_app
from flask.ext.restful import Api, Resource, fields

app = Flask(__name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp, catch_all_404s=True)

# Marshaled fields for links in meta section
link_fields = {
    'prev': fields.String,
    'next': fields.String,
    'first': fields.String,
    'last': fields.String,
}

# Marshaled fields for meta section
meta_fields = {
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total': fields.Integer,
    'pages': fields.Integer,
    'links': fields.Nested(link_fields)
}

from .resources import (
    auth,
    user,
    task,
)

@api.resource('/')
class Index(Resource):
    def get(self):
        apidict = {
            'bet_url':"/bets/{id}",
        }
        return apidict
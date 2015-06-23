# -*- coding:utf-8 -*-
'''
Created on 2015年6月22日

@author: nob
'''
from flask import current_app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from .database import (
    db,
    Model,
    SurrogatePK,
)

class User(SurrogatePK, Model):
    __tablename__ = 'user'
    phone = db.Column(db.String(16), index=True)
    nickname = db.Column(db.String(64))
    password = db.Column(db.String(77)) # real is hash_password

    def __init__(self, phone, nickname, password, **kwargs):
        db.Model.__init__(self, phone=phone, nickname=nickname, **kwargs)
        self.hash_password(password)

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password) # len(s)=77

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=3600): # day:86400 month:2592000
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        self.token = s.dumps({'id': self.id}) # len(token)=123
        return self.token

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token) # {u'id': 2}
        except SignatureExpired:
            print 'expired'
            return None    # valid token, but expired
        except BadSignature:
            print 'invalid'
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

    @classmethod
    def get_by_phone(cls, phone):
        return cls.query.get(phone)

    def __repr__(self):
        return '<User %s, %r, %r>' % (self.id, self.nickname, self.password)


class Task(SurrogatePK, Model):
    __tablename__ = 'tasks'
    # Define a foreign key relationship to a User object
    user_id = db.Column(db.ForeignKey("user.id"), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    summary = db.Column(db.String(512), nullable=True)
    description = db.Column(db.String(1024), nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)
# -*- coding:utf-8 -*-
'''
Created on 2015年6月23日

@author: nob
'''
def user_to_dict(user):
    return {
        'id':user.id,
        'phone':user.phone,
        'nickname':user.nickname,
    }
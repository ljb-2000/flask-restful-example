# -*- coding:utf-8 -*-
'''
Created on 2015年6月22日

@author: nob
'''
from game import create_app

app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8088)
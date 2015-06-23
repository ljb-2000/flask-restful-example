# -*- coding:utf-8 -*-
from flask import Flask

def create_app():
    app = Flask(__name__)

    # 加载配置
    from .config import Config
    from .extensions import db

    app.config.from_object(Config)
    db.init_app(app)

    # 注册蓝图
    from .api import api_bp
    from .views import home
    app.register_blueprint(api_bp)
    app.register_blueprint(home)

    # 注册钩子方法
    app.before_request(init_user)
    return app

def init_user():
    pass
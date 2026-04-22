import os
from flask import Flask
from config import Config
from app.models import db
from app.routes import register_blueprints

def create_app():
    # 初始化 Flask 實例
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化擴充套件 (如 SQLAlchemy)
    db.init_app(app)

    # 註冊 Blueprints 路由
    register_blueprints(app)

    return app

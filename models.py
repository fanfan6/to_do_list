# !/usr/bin/python
# coding=utf-8
"""模型类，定义项目需要的数据库字段"""

import time
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin


db = SQLAlchemy()
login_manager = LoginManager()


class ToDoList(db.Model):
    __tablename__ = 'todolist'
    # id 为主键，其它不能为空
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(1024), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, title, status):
        self.user_id = user_id
        self.title = title
        self.status = status
        self.create_time = time.time()


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(24), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

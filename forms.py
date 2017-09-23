# coding=utf-8
"""表单。提交任务表单及登录表单"""

from __future__ import unicode_literals
# __future__模块：把下一版本的新特性导入到当前版本
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length


class ToDoListForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 64)])
    status = RadioField('是否完成', validators=[DataRequired()], choices=[('1', '是'), ('2', '否')])
    submit = SubmitField('提交')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 24)])
    password = StringField('密码', validators=[DataRequired(), Length(1, 24)])
    submit = SubmitField('登录')

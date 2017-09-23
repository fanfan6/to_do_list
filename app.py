# coding=utf-8

from __future__ import unicode_literals

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_login import login_required, login_user, logout_user, current_user

from forms import ToDoListForm, LoginForm
from models import db, login_manager, ToDoList, User

SECRET_KEY = 'fanfan'

# 实例化
app = Flask(__name__)
bootstrap = Bootstrap(app)

# 连接数据库
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:mysql@127.0.0.1:3306/todolist"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route('/', methods=['GET', 'POST'])
@login_required
def show_todolist():
    form = ToDoListForm()
    if request.method == 'GET':
        todolist = ToDoList.query.all()
        return render_template('index.html', todolist=todolist, form=form)
    else:
        if form.validate_on_submit():
            todolist = ToDoList(current_user.id, form.title.data, form.status.data)
            db.session.add(todolist)
            db.session.commit()
            flash('增加成功')
        else:
            flash(form.errors)
        return redirect(url_for('show_todolist'))


@app.route('/delete/<int:id>')
@login_required
def delete_todolist(id):
    todolist = ToDoList.query.filter_by(id=id).first_or_404()
    db.session.delete(todolist)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('show_todolist'))


@app.route('/change/<int:id>', methods=['GET', 'POST"'])
@login_required
def change_todolist(id):
    if request.method == 'GET':
        todolist = ToDoList.query.filter_by(id=id).first_or_404()
        form = ToDoListForm()
        form.title.data = todolist.title
        form.status.data = str(todolist.status)
        return render_template('modify.html', form=form)
    else:
        form = ToDoListForm()
        if form.validate_on_submit():
            todolist = ToDoList.query.filter_by(id=id).first_or_404()
            todolist.title = form.title.data
            todolist.status = form.status.data
            db.session.commit()
            flash('添加成功')
        else:
            flash(form.errors)
        return redirect(url_for('show_todolist'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            login_user(user)
            flash('登录成功')
            return redirect(url_for('show_todolist'))
        else:
            flash('用户名或密码错误')
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功')
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


if __name__ == '__main__':
    app.run(debug=True)

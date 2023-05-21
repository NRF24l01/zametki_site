from flask import Flask, session, redirect, render_template, abort, request
from sqlite_defs import *
from config import *

app = Flask(__name__)
app.secret_key = 'Stas_krutoy'


# Страница со списком задач

@app.route('/')
def index():
    return redirect('/login')


@app.route('/tasks/add', methods=['post'])
def add_task():
    task_name = request.form.get('task_name')
    task_description = request.form.get('task_description', '')
    user_name = session.get('name', False)
    print(task_name, task_description)

    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/login', methods=['post'])
def login_post():
    #print(request.form)
    user_name = request.form.get('username')
    password = request.form.get('password')
    suc = login(user_name, password)
    if suc:
        session['name'] = user_name
        session['pass'] = password
        return redirect('/tasks')
    else:
        session.clear()
        return render_template('login.html', fleksim='ИМЯ ПОЛЬЗАВАТЕЛЯ ИЛИ ПАРОЛЬ ИНВАЛИДЫ')


@app.route('/login', methods=['get'])
def login_get():
    session['auth'] = True
    return render_template('login.html', fleksim='')


app.run(debug=True, port='8000', host='0.0.0.0')

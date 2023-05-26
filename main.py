from flask import Flask, session, redirect, render_template, abort, request
from sqlite_defs import *
from config import *

app = Flask(__name__)
app.secret_key = 'Stas_krutoy'


# Страница со списком задач

@app.route('/')
def index():
    if session.get('name') == None:
        return redirect('/login')
    else:
        return redirect('/tasks')


@app.route('/tasks')
def watch_task():
    user_name = session.get('name')
    #print(user_name)
    tasks = get_task_list(user_name)
    print(tasks)
    done_count = len([task for task in tasks if task['is_done']])
    count = len(tasks)
    return render_template("tasks.html", tasks=tasks, done_count=done_count, count=count)

@app.route('/tasks/add', methods=['post'])
def add_task():
    task_name = request.form.get('task_name')
    task_description = request.form.get('task_description', '')
    user_name = session.get('name', False)
    #print(task_name, task_description, user_name)
    new_zametka(user_name, task_name, task_description)

    return redirect('/tasks')

@app.route('/tasks/<int:id>/delete')
def make_del(id):
    tasks = get_task_list(session.get('name'))
    if id < 0 or id >= len(tasks):
        abort(404)
    rid = int(tasks[id]["real_id"])
    print(rid, id, tasks[id])

    upd_zametka(rid, "del", "True")

    return redirect('/')

@app.route('/tasks/<int:id>/undone')
def make_undone(id):
    tasks = get_task_list(session.get('name'))
    if id < 0 or id >= len(tasks):
        abort(404)
    rid = int(tasks[id]["real_id"])
    print(rid, id, tasks[id])

    upd_zametka(rid, "state", "False")

    return redirect('/')

@app.route('/tasks/<int:id>/done')
def make_done(id):
    tasks = get_task_list(session.get('name'))
    if id < 0 or id >= len(tasks):
        abort(404)
    rid = int(tasks[id]["real_id"])
    print(rid, id, tasks[id])

    upd_zametka(rid, "state", "True")

    return redirect('/')

@app.route('/tasks/<int:id>/edit', methods=['get'])
def edit_task_page(id):
    tasks = get_task_list(session.get('name'))
    if id < 0 or id >= len(tasks):
        abort(404)
    # Передаем в шалон текущие параметры задачи
    return render_template('edit.html', task=tasks[id], task_id=id)

@app.route('/tasks/<int:id>/edit', methods=['post'])
def edit_task(id):
    tasks = get_task_list(session.get('name'))
    if id < 0 or id >= len(tasks):
        abort(404)

    task_name = request.form.get('task_name')
    task_description = request.form.get('task_description', '')
    rid = int(tasks[id]["real_id"])

    upd_zametka(rid, "title", task_name)
    upd_zametka(rid, "text", task_description)

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
    #print(suc)
    if suc:
        session['name'] = user_name
        session['pass'] = password
        return redirect('/tasks')
    else:
        session.clear()
        return render_template('login.html', fleksim='ИМЯ ПОЛЬЗАВАТЕЛЯ ИЛИ ПАРОЛЬ ИНВАЛИДЫ')

@app.route('/login', methods=['get'])
def login_get():
    #print(session.get('auth'), type(session.get('auth')))
    if session.get('auth') != None:
        return redirect('/tasks')
    else:
        return render_template('login.html', fleksim='',name="Ваше имя пользователя", passw='Ваш пароль')


app.run(debug=True, port='80', host='0.0.0.0')

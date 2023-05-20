from flask import Flask, session, redirect,  render_template,  abort, request
from sqlite_defs import *

app = Flask(__name__)
app.secret_key = 'Stas_krutoy'

# Страница со списком задач
@app.route('/')
def index():
    done_count = len([task for task in tasks if task['is_done']])
    count = len(tasks)
    return render_template("tasks.html", tasks=tasks, done_count=done_count, count=count)
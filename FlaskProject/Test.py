from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = '9b2856b07f83428988d154fe9f927df7c1c12a7cab99e7d9'
messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]
connection = sqlite3.connect("messages.db", check_same_thread=False)
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS messages (title TEXT, content TEXT)")


@app.route('/')
def index():
    messagesDB = cursor.execute("SELECT title, content FROM messages").fetchall()
    return render_template('index.html', messages=messagesDB)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required')
        elif not content:
            flash('Content is required')
        else:
            messages.append({'title': title, 'content': content})
            cursor.execute("INSERT INTO messages VALUES (?,?)", (title, content))
            return redirect(url_for('index'))
    return render_template('create.html')

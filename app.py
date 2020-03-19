from flask import Flask, render_template, request, url_for, redirect, session
from sqlite3 import IntegrityError
from db import app_db, add_user, login_user, get_user_id, add_task, get_tasks,delete_task

app = Flask(__name__)
app.secret_key = 'etovcesecretno'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        check_password = request.form['check_password']
        if password != check_password:
            return render_template('index.html', error="different_passwords") 
            
        try:
            add_user(name, email, password)
        except IntegrityError:
            return render_template('index.html', error="already_exists")
            
        session['human'] = name
        return redirect(url_for('user_page', name = session['human']))

    return render_template('index.html') #<h>, </h> - теги HTML


@app.route('/users/<name>', methods=['GET', 'POST']) #в <> определяем name, котороое мы можем использовать 
def user_page(name):
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        end_date = request.form['end_date']
        user_id = get_user_id(name)
        add_task(user_id, title, content, end_date)
    user_tasks = get_tasks(name)
    return render_template('user.html', username = name, tasks = user_tasks)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        user = login_user(email, password)
        if not user:
            return render_template('login.html', error=True)
        session['human'] = user[1]
        return redirect(url_for('user_page', name=user[1] ))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('human', None)
    return redirect(url_for('index'))




@app.route('/delete/<id>')
def delete(id):
    username = session['human']
    delete_task(username, id)
    return redirect(url_for('user_page', name=username))


if __name__ == "__main__":
    app.run(debug = True)

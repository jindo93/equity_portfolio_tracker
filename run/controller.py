#!/usr/bin/env python3
from model.user import User
from model.admin import Admin
from flask import Flask, render_template, request, session, redirect, url_for
# importing a class from a module, which is a third-party library.

app = Flask(__name__)
# Creating an instance of the Flask class and assigning it to the app variable.
app.secret_key = 'random'
file = 'run/datafile.db'


@app.route('/', methods=['GET'])
def frontpage():
    if 'username' in session:
        return redirect('/user-home')
    elif 'admin' in session:
        return redirect('/admin-home')
    else:
        return render_template('index.html')  # redirect('/login')


@app.route('/user-login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user_login.html', msg='Enter username and password')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(file)
        if user.login(username, password):
            session['username'] = username
            return redirect(url_for('user_home'))
        else:
            return render_template(
                'user_login.html', msg='Invalid user credentials'
            )


@app.route('/user-logout', methods=['GET'])
def log_out():
    session.pop('username', None)
    return render_template('index.html')


@app.route('/update-balance', methods=['POST'])
def update_balance():
    deposit = request.form['deposit']
    user = User(file)


@app.route('/user-home', methods=['GET', 'POST'])
def user_home():
    if request.method == 'GET':
        user = User(file)
        user.initialize_user(session['username'])
        return render_template(
            'user_home.html',
            usr=user.username,
            balance=user.balance,
            positions=user.positions,  # session['positions'],
            earnings=user.earnings
        )


@app.route('/signup', methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        return render_template('signup.html', msg='Check if username exists')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(file)
        if user.query_username(username):
            return render_template(
                'signup.html', msg='Username already exists!'
            )
        else:
            user.signup(username, password)
            return render_template(
                'login.html', msg='Enter username and password'
            )


@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template(
            'admin_login.html', msg='Enter admin username and password'
        )
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin()
        if admin.login(username, password):
            session['admin'] = username
            return redirect(url_for('admin_home'))
        else:
            return render_template(
                'admin_login.html',
                msg='Invalid Credentials'
            )


@app.route('/admin-home', methods=['GET', 'POST'])
def admin_home():
    if request.method == 'GET':
        admin = Admin()
        admin.initialize_admin(session['admin'])
        return render_template(
            'admin_home.html',
        )


@app.route('/leaderboard')
def leaderboard():
    pass


if __name__ == '__main__':
    app.run(port=5001)

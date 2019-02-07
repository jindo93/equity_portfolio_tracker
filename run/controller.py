#!/usr/bin/env python3
from model.user import User
from model.admin import Admin
from flask import Flask, render_template, request
# importing a class from a module, which is a third-party library.

app = Flask(__name__)
# Creating an instance of the Flask class and assigning it to the app variable.

file = 'run/datafile.db'


@app.route('/')
def frontpage():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', msg='Enter username and password')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(file)
        if not user.login(username, password):
            return render_template(
                'login.html', msg='Invalid user credentials'
            )
        else:
            return render_template(
                'user_home.html',
                usr=username,
                balance=user.balance
            )

        if username == 'jin' \
                and password == '0000':
            return render_template(
                'user_home.html', msg='User credentials confirmed', usr=username
            )
        else:
            return render_template('login.html', msg='Invalid credentials')
    pass


@app.route('/user-home', methods=['GET', 'POST'])
def user_home():
    if request.method == 'GET':
        return render_template('user_home.html', msg='')


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


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template(
            'admin.html', msg='Enter admin username and password'
        )
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'jin' and password == '0000':
            return 'Admin credentials confirmed'
        else:
            return 'Invalid credentials'


@app.route('/leaderboard')
def leaderboard():
    pass


if __name__ == '__main__':
    app.run()

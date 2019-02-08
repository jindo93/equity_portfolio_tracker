#!/usr/bin/env python3
from model.user import User
from model.admin import Admin
from flask import Flask, render_template, request, session
# importing a class from a module, which is a third-party library.

app = Flask(__name__)
# Creating an instance of the Flask class and assigning it to the app variable.
app.secret_key = 'random'

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
        user.login(username, password)
        if user:
            session['username'] = username
            session['password'] = password
            session['user_id'] = user.user_id
            session['balance'] = user.balance
            session['positions'] = {}
            session['positions'] = user.positions
            session['earnings'] = {}
            session['earnings'] = user.earnings

            return render_template(
                'user_home.html',
                usr=session['username'],
                balance=session['balance'],
                positions=session['positions'],
                earnings=session['earnings']
            )
            # return redirect(url_for('user_home.html'))
        else:
            return render_template(
                'login.html', msg='Invalid user credentials'
            )
        # else:
        #     return render_template(
        #         'user_home.html',
        #         usr=username,
        #         balance=user.balance
        #     )


@app.route('/update-balance', methods=['POST'])
def update_balance():
    deposit = request.form['deposit']
    user = User(file)


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
    app.run(port=5001)

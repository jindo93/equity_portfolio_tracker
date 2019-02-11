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
    user_logout()
    admin_logout()
    if 'username' in session:
        return redirect('/user-home')
    elif 'admin' in session:
        return redirect('/admin-home')
    else:
        return render_template('index.html')  # redirect('/login')


@app.route('/user-login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template(
            'user_login.html', msg='Enter username and password'
        )
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
        #print('before login')
        if admin.login(username, password):
            #print('after login')
            session['admin'] = username
            return redirect(url_for('admin_home'))
        else:
            return render_template(
                'admin_login.html', msg='Invalid Credentials'
            )


@app.route('/user-logout', methods=['GET'])
def user_logout():
    session.pop('username', None)
    return render_template('index.html')


@app.route('/admin-logout', methods=['GET'])
def admin_logout():
    session.pop('admin', None)
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        return render_template('signup.html')
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
                'user_login.html',
                msg='Successfully signed up! Enter username and password to login'
            )


@app.route('/deposit', methods=['POST'])
def deposit():
    if request.method == 'POST':
        user = User(file)
        user.initialize_user(session['username'])
        amount = request.form.get('deposit')
        amount = int(amount)
        if amount > 0:
            user.deposit(amount)
            return redirect('/user-home')
        else:
            render_template('user_home.html', msg="Error")


@app.route('/withdraw', methods=['POST'])
def withdraw():
    if request.method == 'POST':
        user = User(file)
        user.initialize_user(session['username'])
        amount = request.form.get('withdraw')
        amount = int(amount)
        if amount > 0:
            user.withdraw(amount)
            return redirect('/user-home')
        else:
            render_template('user_home.html', msg="Error")


@app.route('/user-home', methods=['GET', 'POST'])
def user_home():
    if request.method == 'GET':
        user = User(file)
        user.initialize_user(session['username'])
        prices = {}
        stocks = {}
        stocks = user.positions
        for key in stocks:
            prices[key] = [stocks[key], user.quote_last_price2(key)]

        return render_template(
            'user_home.html',
            usr=user.username,
            balance=user.balance,
            positions=prices,
            symbol="",
            price=""
        )


@app.route('/trade-stock', methods=['GET'])
def trade_stock():
    if request.method == 'GET':
        return render_template('trade_stock.html')


@app.route('/buy-stocks', methods=['GET', 'POST'])
def buy_stocks():
    if request.method == 'POST':
        ticker = request.form.get('ticker_symbol')
        amount = int(request.form.get('num_of_stocks'))
        user = User(file)
        user.initialize_user(session['username'])
        if user.buy_stocks(ticker, amount):
            return render_template(
                'trade_stock.html',
                buy_msg='Stocks bought successfully'
            )
        else:
            return render_template(
                'trade_stock.html',
                buy_msg='Transaction failed due to insufficient amount of balance'
            )


@app.route('/sell-stocks', methods=['GET', 'POST'])
def sell_stocks():
    if request.method == 'POST':
        ticker = request.form.get('ticker_symbol')
        amount = int(request.form.get('num_of_stocks'))
        user = User(file)
        user.initialize_user(session['username'])
        if user.sell_stocks(ticker, amount):
            return render_template(
                'trade_stock.html',
                sell_msg='Stocks sold successfully'
            )
        else:
            return render_template(
                'trade_stock.html',
                sell_msg='Transaction failed due to insufficient amount of stocks'
            )


@app.route('/quote-stock-price', methods=['POST'])
def quote_stock_price():
    if request.method == 'POST':
        ticker = request.form.get('ticker_symbol')
        if ticker:
            stock_price = User(file).quote_last_price2(ticker)
            return render_template('trade_stock.html', price=stock_price)


@app.route('/search-ticker', methods=['POST'])
def search_stock():
    if request.method == 'POST':
        company = request.form.get('company_name')
        if company:
            ticker = User(file).lookup_ticker_symbol(company)
            return render_template('trade_stock.html', symbol=ticker)
        else:
            return render_template('trade_stock.html')

# @app.route('/search-ticker', methods=['POST'])
# def search_ticker():
#     if request.methods == 'POST':
#         user = User(file)
#         user.initialize_user(session['username'])
#         company_name = request.form.get(company_name)
#         ticker = user.lookup_ticker_symbol(company_name)
#         return redirect(url_for('user_home'))


@app.route('/admin-home', methods=['GET', 'POST'])
def admin_home():
    if request.method == 'GET':
        admin = Admin()
        admin.initialize_admin(session['admin'])
        return render_template(
            'admin_home.html',
            leaderboard=admin.leaderboard  # admin.leaderboard
        )


@app.route('/leaderboard')
def leaderboard():
    pass


if __name__ == '__main__':
    app.run(port=5003)

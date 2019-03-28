#!/usr/bin/env python3

import time

from mapper import Schema
from wrapper import Markit


class User:

    def __init__(self, file_name):
        self.file_name = file_name
        self.user_id = 0
        self.username = ""
        self.password = ""
        self.balance = 0.00
        self.positions = {}
        self.earnings = {}
        self.net_profit = {}

    # TODO check usage
    def login(self, username, password):
        if self.confirm_user(username, password):
            with Schema(self.file_name) as db:
                users = db.login(username, password)
                self.user_id = users[0][0]
                self.username = users[0][1]
                self.password = users[0][2]
                self.balance = users[0][3]
                self.positions = db.query_positions(self.user_id)
            return True
        return False

    def initialize_user(self, username):
        if self.query_username(username):
            with Schema(self.file_name) as db:
                user = db.initialize_user(username)
                self.user_id = user[0][0]
                self.username = user[0][1]
                self.password = user[0][2]
                self.balance = user[0][3]
                self.positions = db.query_positions(self.user_id)
                self.net_profit = self.get_each_earnings()
            return True
        return False

    # holdings value net gain/loss
    def get_dashboard(self):
        dashboard = {}
        positions = self.positions
        net_profit = self.net_profit
        for i, k in enumerate(positions):
            key = k.upper()
            value = positions[k]*self.quote_last_price2(k)
            dashboard[key] = [positions[k], value, i+1, value+net_profit[k]]

        return dashboard

    def signup(self, username, password):
        with Schema(self.file_name) as db:
            return db.signup(username, password)

    def register_group(self):
        pass

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.update_balance()
            return True
        return False

    def deposit(self, amount):
        self.balance += amount
        self.update_balance()
        return True

    def buy_stocks(self, ticker, num_of_shares):
        broker_fee = 6.95
        last_price = self.quote_last_price(ticker)
        type = 'buy'
        transaction_cost = (last_price * num_of_shares) + broker_fee
        timestamp = time.time()

        if self.balance > transaction_cost:
            if self.search_position_id(ticker):
                self.balance -= transaction_cost
                self.positions[ticker] += num_of_shares
                self.record_trade(ticker, type, last_price,
                                  num_of_shares, timestamp)
                # records new trade in sql trades table
                # updates position in sql positions table
                self.update_position(ticker)
            else:
                self.balance -= transaction_cost
                self.positions[ticker] = num_of_shares
                self.record_trade(ticker, type, last_price,
                                  num_of_shares, timestamp)
                # records new trade in sql trades table
                self.record_position(ticker, num_of_shares)
                # records new position in sql positions table
            self.update_balance()
            return True
        else:
            return False

    def sell_stocks(self, ticker, num_of_shares):
        broker_fee = 6.95
        last_price = self.quote_last_price(ticker)
        type = 'sell'
        timestamp = time.time()
        if self.positions.get(ticker) == None:
            return False

        if self.balance > broker_fee:
            if self.positions.get(ticker) >= num_of_shares:
                self.positions[ticker] -= num_of_shares
                self.balance += (last_price * num_of_shares) - broker_fee
                self.record_trade(ticker, type, last_price,
                                  num_of_shares, timestamp)
                self.update_position(ticker)
                self.update_balance()
                return True
        return False

    def lookup_ticker_symbol(self, company_name):
        with Markit() as m:
            ticker_symbol = m.lookup(company_name.lower())
            if isinstance(ticker_symbol, bool):
                return False
            return ticker_symbol

    def quote_last_price(self, ticker_symbol):
        with Markit() as m:
            last_price = m.quote(ticker_symbol.lower())
            if isinstance(last_price, bool):
                return False
            return last_price

    def quote_last_price2(self, ticker_symbol):
        with Markit() as m:
            last_price = m.quote_price2(ticker_symbol.lower())
            if isinstance(last_price, bool):
                return False
            return last_price

    def query_username(self, username):
        with Schema(self.file_name) as db:
            return db.query_username(username)

    def query_positions(self, username):
        with Schema(self.file_name) as db:
            return db.query_positions(username)

    # TODO TEST username_search
    def username_search(self, username):
        with Schema(self.file_name) as db:
            username_list = db.query_table('users')
        for user in username_list:
            if user[0] == username:
                return True
        return False

    # TODO TEST confirm_user
    def confirm_user(self, username, password):
        with Schema(self.file_name) as db:
            db.cursor.execute(
                '''SELECT user_id
                    FROM users
                    WHERE username = '{0}' AND password = '{1}';'''.format(username, password)
            )
            users = db.cursor.fetchall()
            if len(users) == 1:
                return True
            else:
                return False

    def get_each_earnings(self):
        position_value = {}
        buy_trade = self.get_buy_trades()
        sell_trade = self.get_sell_trades()
        for k in self.positions:
            print('key: ', k)
            if position_value.get(k) == None:
                if sell_trade.get(k):
                    position_value[k] = sell_trade[k]
                if buy_trade.get(k):
                    position_value[k] = -buy_trade[k]
            else:
                if sell_trade.get(k):
                    position_value[k] += sell_trade[k]
                if buy_trade.get(k):
                    position_value[k] -= buy_trade[k]
        return position_value

    def get_total_earnings(self):
        earnings = self.net_profit
        total = 0
        for k in earnings:
            total += earnings[k]
        return total

    def get_sell_trades(self):
        trade_dict = {}
        with Schema(self.file_name) as db:
            trade_dict = db.get_sell_trades(self.user_id)
        return trade_dict

    def get_buy_trades(self):
        trade_dict = {}
        with Schema(self.file_name) as db:
            trade_dict = db.get_buy_trades(self.user_id)
        return trade_dict

    def record_trade(self, ticker, type, stock_price, num_of_shares, timestamp):
        with Schema(self.file_name) as db:
            sql = ''' INSERT INTO trades(
                        user_id, ticker, type, stock_price, num_of_shares, timestamp
                    ) VALUES (?,?,?,?,?,?);'''
            db.cursor.execute(sql, (self.user_id, ticker, type,
                                    stock_price, num_of_shares, timestamp))

    def record_position(self, ticker, num_of_shares):
        with Schema(self.file_name) as db:
            sql = ''' INSERT INTO positions(
                        ticker, num_of_shares, user_id
                    ) VALUES (?,?,?);'''
            db.cursor.execute(sql, (ticker, num_of_shares, self.user_id))

    def update_balance(self):
        with Schema(self.file_name) as db:
            sql = ''' UPDATE users
                        SET balance = {0}
                        WHERE user_id = {1};'''.format(self.balance, self.user_id)
            db.cursor.execute(sql)

    def search_position_id(self, ticker):
        try:
            with Schema(self.file_name) as db:
                sql = '''SELECT position_id
                            FROM positions
                            WHERE user_id = "{0}"
                            AND ticker = "{1}";'''.format(self.user_id, ticker)
                db.cursor.execute(sql)
                id = db.cursor.fetchall()
                return id[0][0]
        except:
            return False

    def update_position(self, ticker):
        position_id = self.search_position_id(ticker)
        print('this works ', position_id)
        with Schema(self.file_name) as db:
            sql = ''' UPDATE positions
                        SET  num_of_shares = {0}
                        WHERE user_id = {1} AND ticker = '{2}' AND position_id = {3};'''
            db.cursor.execute(sql.format(
                self.positions[ticker], self.user_id, ticker, position_id))


###########################################################


    def change_password(self, new_password):
        with Schema(self.file_name) as db:
            sql = ''' UPDATE users
                        SET username = {0},
                            password = {1},
                            balance = {2}
                        WHERE user_id = {3};'''.format(
                self.username,
                self.password,
                self.balance,
                self.user_id
            )
            db.cursor.execute(sql)

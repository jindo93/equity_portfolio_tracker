#!/usr/bin/env python3
import json
from models.mapper import Schema
from models.wrapper import Markit
from models.user import User


class Admin:

    def __init__(self):
        self.username = ""
        self.password = ""
        self.filename = 'run/datafile.db'
        self.admins = 'admins.json'
        self.leaderboard = []

    def login(self, username, password):
        with open(self.admins, 'r') as file:
            data = json.load(file)
        admin_dic = data[username]
        if password != admin_dic['password']:
            return False
        return True

    def initialize_admin(self, username):
        '''leaderboard is is initialized successfully.'''
        #admin = Admin()
        self.username = username
        with open(self.admins, 'r') as file:
            data = json.load(file)
        admin_dic = data[username]
        self.password = admin_dic['password']
        self.filename = self.filename
        self.admins = self.admins
        self.leaderboard = self.get_leaderboard()
        return True

    def delete_user(self, table_name, user_name):
        with Schema(self.filename) as db:
            db.delete_user(table_name, user_name)

    def create_table(self, table_name):
        with Schema(self.filename) as db:
            db.create_table(table_name)
            return True
        return False

    def add_column(self, table_name, column_name, column_type):
        with Schema(self.filename) as db:
            db.add_column(table_name, column_name, column_type)
            return True
        return False

    def delete_table(self, table_name):
        with Schema(self.filename) as db:
            return db.delete_table(table_name)

    @staticmethod
    def getKey(item):
        return item[2]

    # def get_leaderboard(self):
    #     with Schema(self.filename) as db:
    #         sql = '''SELECT username FROM users;'''
    #         db.cursor.execute(sql)
    #         usernames = db.cursor.fetchall()
    #     names = []
    #     for username in usernames:
    #         names.append(username[0])

    #     earnings = []
    #     for name in names:
    #         earning = self.get_total_earnings(name)
    #         earnings.append((name, earning))
    #     sorted(earnings, key=self.getKey, reverse=True)
    #     leaderboard = earnings[:10]

    #     return leaderboard

    def quote_last_price(self, ticker_symbol):
        with Markit() as m:
            ticker = ticker_symbol.lower()
            last_price = m.quote_price2(ticker)
            if isinstance(last_price, bool):
                return False
            return last_price

    def calculate_earnings(self, userid):
        position_dict = {}
        with Schema(self.filename) as db:
            position_dict = db.query_positions(userid)
            total_earnings = 0
            for key in position_dict:
                stock_price = self.quote_last_price(key)
                total_earnings += position_dict[key]*stock_price
            return total_earnings

    def get_leaderboard(self):
        '''Returns a leaderboard with top 10 users'''
        with Schema(self.filename) as db:
            sql = '''SELECT user_id, username FROM users;'''
            db.cursor.execute(sql)
            users = db.cursor.fetchall()
            earnings = []
            for user in users:
                earning = self.calculate_earnings(user[0])
                earnings.append((user[0], user[1], earning))
            sorted_earnings = sorted(earnings, key=self.getKey, reverse=True)
            leaderboard = sorted_earnings[:10]
            return leaderboard

    def query_positions(self, userid):
        with Schema(self.filename) as db:
            return db.query_positions(userid)

    # function created for testing
    def create_terminal_trader_tables(self):
        with Schema(self.filename) as db:
            db.cursor.execute('''DROP TABLE IF EXISTS users;''')
            db.cursor.execute('''DROP TABLE IF EXISTS positions;''')
            db.cursor.execute('''DROP TABLE IF EXISTS trades;''')
            sql_users = '''CREATE TABLE users(
                                user_id         INTEGER PRIMARY KEY AUTOINCREMENT,
                                username        VARCHAR,
                                password        VARCHAR,
                                balance         FLOAT
                            );'''
            db.cursor.execute(sql_users)
            sql_positions = '''CREATE TABLE positions(
                                position_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                                ticker          VARCHAR,
                                num_of_shares   INTEGER,
                                user_id         INTEGER,
                                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                            );'''
            db.cursor.execute(sql_positions)
            sql_trades = '''CREATE TABLE trades(
                                trade_id        INTEGER PRIMARY KEY AUTOINCREMENT,
                                type            VARCHAR,
                                ticker          VARCHAR,
                                stock_price     FLOAT,
                                num_of_shares   INTEGER,
                                timestamp       FLOAT,
                                user_id         INTEGER,
                                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                        );'''
            db.cursor.execute(sql_trades)


# if __name__ == '__main__':
    # Admin('demo.db').create_terminal_trader_tables()
    # admin = Admin()
    # admin.login('yjd', '0000')

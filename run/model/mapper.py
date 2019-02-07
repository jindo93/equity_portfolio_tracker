#!/usr/bin/env python3

import os
import sqlite3

class Schema:
    def __init__(self,datafile):
        self.connection = sqlite3.connect(datafile,check_same_thread=False)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.connection:
            if self.cursor:
                self.connection.commit()
                self.cursor.close()
            self.connection.close()

    def create_table(self, table_name):
        try:
            sql = ''' CREATE TABLE "{0}"(
                        pk INTEGER PRIMARY KEY AUTOINCREMENT
                    );'''.format(table_name)
            self.cursor.execute(sql)
            return True
        except:
            return False

    def add_column(self, table_name, column_name, column_type):
        try:
            sql = ''' ALTER TABLE "{0}"
                        ADD COLUMN "{1}" "{2}"
                    ;'''.format(table_name, column_name, column_type)
            self.cursor.execute(sql)
            return True
        except:
            return False

    def delete_table(self, table_name):
        try:
            self.cursor.execute(
                '''DROP TABLE IF EXISTS "{0}";'''.format(table_name))
            return True
        except:
            return False

    def query_table(self, table_name):
        try:
            sql = '''SELECT username
                        FROM "{0}";'''.format(table_name)
            self.cursor.execute(sql)
            user_list = self.cursor.fetchall()
            return user_list
        except:
            return False
        
    def query_userinfo(self):
        try:
            sql = '''SELECT *
                        FROM users;'''
            self.cursor.execute(sql)
            users_list = self.cursor.fetchall()
            return users_list
        except:
            return False

    def delete_user(self, table_name, user_name):
        try:
            sql = ''' DROP *
                        FROM "{0}"
                        WHERE username = "{1}";'''.format(table_name, user_name)
            self.cursor.execute(sql)
            return True
        except:
            return False

    def query_username(self, user_name):
        try:
            sql = ''' SELECT *
                        FROM users
                        WHERE username = "{0}";'''.format(user_name)
            self.cursor.execute(sql)
            user = self.cursor.fetchall()
            if len(user) == 1:
                return True
        except:
            return False

    def query_position(self, username, ticker):
        try:
            sql = ''' SELECT ticker, num_of_shares
                        FROM positions
                        WHERE user_id =
                            (SELECT user_id
                                FROM users
                                WHERE username = ?)
                        AND ticker = ?;'''
            return self.cursor.execute(sql, (username, ticker))
        except:
            return False

    def query_positions(self, username):
        try:
            sql = ''' SELECT *
                        FROM positions
                        WHERE user_id = (SELECT user_id
                                        FROM users
                                        WHERE username = "{0}")
                        GROUP BY ticker;'''.format(username)
            self.cursor.execute(sql)
            positions = self.cursor.fetchall()
            position_dict = {}
            for position in positions:
                position_dict[position[1]] = position[2]
            return position_dict
        except:
            return False


    def get_sell_trades(self, username):
        try:
            sql = ''' Select *
                        FROM trades
                        WHERE type = 'sell'
                        AND user_id =
                                (SELECT user_id
                                FROM users
                                WHERE username = "{0}");'''.format(username)
            self.cursor.execute(sql)
            trades = self.cursor.fetchall()
            trades_dict = {}
            for trade in trades:
                trades_dict[trade[0]] = [trade[2],trade[3],trade[4]]
            return trades_dict
        except:
            return False
                        
    def get_buy_trades(self, username):
        try:
            sql = ''' SELECT *
                        FROM trades
                        WHERE user_id =
                            (SELECT user_id
                            FROM users
                            WHERE username = "{0}")
                        AND type = 'buy';'''.format(username)
            self.cursor.execute(sql)
            trades = self.cursor.fetchall()
            trades_dict = {}
            for trade in trades:
                trades_dict[trade[0]] = [trade[2], trade[3], trade[4]]
            return trades_dict
        except:
            return False
    




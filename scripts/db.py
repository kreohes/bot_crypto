import asyncio
import sqlite3

conn = sqlite3.connect('db_for_bot.db')


class Database:
    def __init__(self):
        self.cur = conn.cursor()
    def connection(self, name, act):
        self.cur.execute("INSERT INTO logs(names, action) VALUES(?, ?)", (name, act,))
        conn.commit()

    def check_currencies(self):
        self.cur.execute("""""")

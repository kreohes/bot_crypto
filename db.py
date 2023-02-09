import asyncio
import sqlite3

conn = sqlite3.connect('db_for_bot.db')


class Database:
    def __init__(self):
        self.cur = conn.cursor()

    def connection(self, name, act):
        # отслеживание каждого действия каждого пользователя
        self.cur.execute("INSERT INTO logs(names, action) VALUES(?, ?)", (name, act,))
        conn.commit()

    def add_currencies(self, id_user, currency):
        # привязка валюту к конкретному пользователю
        for num in currency:
            self.cur.execute("""INSERT INTO compilations(id_user,value) VALUES(?,?)""", (id_user, num))
        conn.commit()

    def all_currencies(self):
        # получение списка всех возможных валют
        return self.cur.execute("""SELECT charcode FROM currencies""")

    def check_currencies(self, id_user):
        # получение валют выбранных пользователем
        value = self.cur.execute("""SELECT value FROM compilations WHERE id_user=?""", (id_user,)).fetchall()
        value_list = []
        for num in value:
            value_list.append(
                *self.cur.execute("""SELECT names FROM currencies WHERE id =?""", (num[0],)).fetchall()[0])
        return value_list

    def correct_currencies(self, valute, id_user=0, param='find'):
        result = self.cur.execute("""SELECT charcode,id FROM currencies WHERE names =?""", (valute,)).fetchall()
        if param == 'find':
            return result[0]
        elif param == 'add':
            result = self.cur.execute("""SELECT id FROM currencies WHERE charcode =?""", (valute,)).fetchall()
            self.cur.execute("""INSERT INTO compilations(id_user,value) VALUES(?,?)""", (id_user, result[0][0]))
            conn.commit()
            return f'Валюта {valute} успешно добавлена!'
        elif param == 'delete':
            self.cur.execute("""DELETE from compilations WHERE id_user =? AND value=?""", (id_user, result[0][1]))
            conn.commit()
            return f'Валюта {valute} успешно удалена!'

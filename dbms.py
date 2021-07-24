import sqlite3
from flask import g


class SQLite3DatabaseHandler():
    def __init__(self, database):
        self.database = database

    def connect(self):
        return sqlite3.connect(self.database)

    def get_tables(self):
        with self.connect() as db:
            cursor = db.cursor()
            output = cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table';").fetchall()

        return output

    def create_table(self, challenge_num,
                     schema="username varchr(37) PRIMARY KEY UNIQUE, language varchar(16) NOT NULL, code varchar(250) NOT NULL"):

        with self.connect() as db:
            cursor = db.cursor()

            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS solution{challenge_num}  ({schema})")
            db.commit()

    def insert_values(self, challenge_num, uname, language, code):
        with self.connect() as db:
            cursor = db.cursor()

            cursor.execute(
                f"INSERT INTO solution{challenge_num} VALUES('{uname}', '{language}', '{code}')")

    def get_values(self, challenge_num):
        with self.connect() as db:
            cursor = db.cursor()

            out = cursor.execute(f"SELECT * FROM solution{challenge_num}")

        return out.fetchall()
 #################login db###############################   

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            "login.db", detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
  
def makelogindb():    
    conn = sqlite3.connect('login.db')

#Creating a cursor object using the cursor() method
    cursor = conn.cursor()

#Doping EMPLOYEE table if already exists.
    cursor.execute("DROP TABLE IF EXISTS user")

#Creating table as per requirement
    sql ="""CREATE TABLE user (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    discriminator TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    profile_pic_url TEXT NOT NULL
    );"""
    cursor.execute(sql)
    

# Commit your changes in the database
    conn.commit()

#Closing the connection
    conn.close()


if __name__ == "__main__":
    db = SQLite3DatabaseHandler('solutions.db')

    print(db.create_table(1))
    print(db.get_tables())
    
    db.insert_values(1, 'user1', 'python',
                     'def solution(n):\n\tprint(n * n)')
    db.insert_values(1, 'user2', 'javascript',
                     'const solution = (n) => {console.log(n * n)}')
    db.insert_values(1, 'user3', 'javascript',
                     'const solution = (n) => {console.log(n * n * n)}')
    db.insert_values(1, 'user5', 'python',
                     'import os\ndef solution(n):\n\tprint(n * n/n)')

    print(db.get_values(1))

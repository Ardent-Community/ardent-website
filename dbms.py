import sqlite3


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

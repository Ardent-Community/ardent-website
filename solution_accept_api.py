from dbms import SQLite3DatabaseHandler


def add_solution(challenge_id, username, solution):
    db = SQLite3DatabaseHandler("./solutions.db")
    db.connect()
    db.create_table(challenge_id)
    db.insert_values(challenge_id, username, solution)

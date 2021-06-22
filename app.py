from flask import Flask, render_template, jsonify, request, abort
import sqlite3


app = Flask(__name__)
db = sqlite3.connect("solutions.db")
cursor = db.cursor()


# TODO: change the name of the solutions table to soething which will represent the challenge
# create table TODO: functonize this
# cursor.execute("CREATE TABLE solutions (username varchr(37) PRIMARY KEY UNIQUE, language varchar(16) NOT NULL, code varchar(250) NOT NULL)")


@app.get("/")
def home():
    return render_template('index.html')


def add_solution(username:str, language:str, code:str):
    """Adds the given information to the database"""
    cursor.execute(f"INSERT INTO solutions VALUES({username}, {language}, {code})")
    cursor.commit()

# TODO: make a function to read tbe db

@app.get('/api/solutions/<int:number>')
def get_challenge_sollution(number):
    # TODO: use real data here
    if request.args.get('api_key') == 'shravanisresponsible':  # TODO: use enfironment variable
        sols = {
            "username1": {
                "language": "python",
                "code": "from time import sleep\nsleep(1)"
            },
            "username2": {
                "language": "javascript",
                "code": "console.log('hey')"
            }
        }

        return jsonify(sols) if number == 1 else jsonify(None), 200  # TODO: make this solution sensible
    abort(404)


@app.errorhandler(404)
def page_not_found(error):  # TODO: better error handelling needed
   return jsonify({"response_code": 404})


if __name__ == '__main__':
    app.run(debug=True)

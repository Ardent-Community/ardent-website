from flask import Flask, render_template, jsonify, request, abort
from dbms import SQLite3DatabaseHandler
import os

"""
* to setup environment variable, execute:
$ export PROBE_API_KEY='supersecretkey'

* check if the env variable got set
$ echo $PROBE_API_KEY 
"""


app = Flask(__name__)
db = SQLite3DatabaseHandler('solutions.db')

# TODO: add solution accepting api

########################## WEBSITE #################################

@app.get("/")
def home():
    return render_template('index.html')


########################## API #################################


def add_solution(username: str, language: str, code: str):
    """Adds the given information to the database"""
    db.insert_values(1, username, language, code)


def get_challenge_solution_data(number):
    data = {"solutions":{}}
    try:
        solutions = db.get_values(number)
    except:
        abort(400)

    for solution in solutions:
        data["solutions"][solution[0]] = {
            "language": solution[1],
            "code": solution[2]
        }

    return data


@app.get('/api/solutions/<int:number>')
def get_challenge_sollution(number):
    if request.args.get('apiKey') == os.environ["PROBE_API_KEY"]:
        return jsonify(get_challenge_solution_data(number))

    abort(404)


@app.errorhandler(404)
def page_not_found(error):  # TODO: better error handelling needed
    return jsonify({"response_code": 404})


@app.errorhandler(400)
def no_data(error):  # TODO: better error handelling needed
    return jsonify({"response_code": 400, "status": "NO data"})


if __name__ == '__main__':
    app.run(debug=True)

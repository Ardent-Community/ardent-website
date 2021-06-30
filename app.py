from flask import Flask, render_template, jsonify, redirect, request, session
from dbms import SQLite3DatabaseHandler
from oauth import OAuth2
import os

"""
* to setup environment variable, execute:
$ export PROBE_API_KEY='supersecretkey'

* check if the env variable got set
$ echo $PROBE_API_KEY 
"""


app = Flask(__name__)
db = SQLite3DatabaseHandler('solutions.db')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# TODO: add solution accepting api

########################## WEBSITE #################################

@app.get("/")
def home():
    code = request.args.get("code")

    authentication_token = OAuth2.get_access_token(code)
    session["token"] = authentication_token

    user = OAuth2.get_user_json(authentication_token)
    # user_name, user_id = user.get("username"), user.get("discriminator")

    return f"Success, logged in as {user}"
    # return render_template('index.html')


@app.get("/login")
def redirect_to_discord():
    return redirect(OAuth2.DISCORD_LOGIN_URL)


########################## API #################################


def add_solution(username: str, language: str, code: str):
    """Adds the given information to the database"""
    db.insert_values(1, username, language, code)


def get_challenge_solution_data(number):
    data = {'ok': True, 'solutions':{}, 'error': '', 'message':''}
    try:
        solutions = db.get_values(number)
    except Exception as e:
        print(e)
        data['ok'] = False
        data['message'] = "Data not found"
        data['error'] = f"Unable to find solutions to challenge {number}"
        return jsonify(data)

    for solution in solutions:
        data["solutions"][solution[0]] = {
            "language": solution[1],
            "code": solution[2]
        }

    data['ok'] = bool(data['solutions'])

    if not data['ok']:
        data['message'] = 'No Data for the challenge'
        data['error'] = f"No data in the database for the challenge {number}"

    return data


@app.get('/api/solutions/<int:number>')
def get_challenge_sollution(number):
    if request.headers.get('API-KEY') == os.environ["PROBE_API_KEY"] and request.headers.get('User-Agent') == 'probe-cli':
        return jsonify(get_challenge_solution_data(number))

    else:
        return jsonify({
            'ok': False,
            'message': "Access denied",
            'error': "Unable to recognize the User-Agent, check the API key",
            'solutions': {}
        })


@app.errorhandler(404)
def page_not_found(error):  # TODO: better error handelling needed
    return jsonify({"response_code": 404})


@app.errorhandler(400)
def no_data(error):  # TODO: better error handelling needed
    return jsonify({"response_code": 400, "status": "NO data"})

@app.errorhandler(500)
def internal_server_error(error):  # TODO: better error handelling needed
    return jsonify({"response_code": 500, "status": "NO data"})


if __name__ == '__main__':
    app.run(debug=True)

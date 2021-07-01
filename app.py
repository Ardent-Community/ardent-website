from flask import Flask, render_template, jsonify, redirect, request, session, url_for
from dbms import SQLite3DatabaseHandler
from requests_oauthlib import OAuth2Session
import getpass
import os



# Settings for your app
base_discord_api_url = 'https://discordapp.com/api'
client_id = os.environ['ID'] # Get from https://discordapp.com/developers/applications
discordkey= os.environ['SECRET']
redirect_uri='http://192.168.1.78:5000/oauth_callback'
scope = ['identify']
token_url = 'https://discordapp.com/api/oauth2/token'
authorize_url = 'https://discordapp.com/api/oauth2/authorize'

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'



app = Flask(__name__)
db = SQLite3DatabaseHandler('solutions.db')
app.config['SECRET_KEY']=discordkey
# TODO: add solution accepting api

def token_updater(token):
    session['oauth2_token'] = token




########################## WEBSITE #################################

@app.route("/")
def home():
    code = request.args.get("code")
    
    

    
@app.route("/login")
def login():
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    login_url, state = oauth.authorization_url(authorize_url)
    session['state'] = state
    print("Login url: %s" % login_url)
    return redirect(login_url)


@app.route("/oauth_callback")
def oauth_callback():
    """
    The callback we specified in our app.
    Processes the code given to us by Discord and sends it back
    to Discord requesting a temporary access token so we can 
    make requests on behalf (as if we were) the user.
    e.g. https://discordapp.com/api/users/@me
    The token is stored in a session variable, so it can
    be reused across separate web requests.
    """
    discord = OAuth2Session(client_id, redirect_uri=redirect_uri, state=session['state'], scope=scope)
    token = discord.fetch_token(
        token_url,
        client_secret=discordkey,
        authorization_response=request.url,
    )
    session['discord_token'] = token
    
    return redirect(url_for('.profile'))
    
    
@app.route("/profile")
def profile():
    """
    Example profile page to demonstrate how to pull the user information
    once we have a valid access token after all OAuth negotiation.
    """
    discord = OAuth2Session(client_id, token=session['discord_token'])
    response = discord.get(base_discord_api_url + '/users/@me').json()
    # https://discordapp.com/developers/docs/resources/user#user-object-user-structure
    return jsonify(user=response)


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

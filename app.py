from flask import Flask, render_template, jsonify, redirect, request, session, url_for
from dbms import SQLite3DatabaseHandler
from requests_oauthlib import OAuth2Session
import os
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from user import User
from dbms import makelogindb

get_avatar = "https://cdn.discordapp.com/avatars/"
# Settings for your app
base_discord_api_url = "https://discordapp.com/api"
client_id = os.environ["ID"]  # Get from https://discordapp.com/developers/applications
discordkey = os.environ["SECRET"]
redirect_uri = "http://192.168.43.234:5000/oauth_callback"
scope = ["identify"]
token_url = "https://discordapp.com/api/oauth2/token"
authorize_url = "https://discordapp.com/api/oauth2/authorize"
seed = os.environ["CODE"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


app = Flask(__name__)
db = SQLite3DatabaseHandler("solutions.db")
app.config["SECRET_KEY"] = discordkey
# TODO: add solution accepting api


def token_updater(token):
    session["oauth2_token"] = token


login_manager = LoginManager()
login_manager.init_app(app)
try:
    makelogindb()
except Exception as e:
    pass


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


########################## WEBSITE #################################


@app.route("/")
def home():
    if current_user.is_authenticated:
        #         return (
        #             "<p>Hello, {}! You're logged in! Email: {}</p>"
        #             "<div><p>Discord Avatar:</p>"
        #             '<img src="{}" alt="Discord avatar"></img></div>'
        #             '<a class="button" href="/logout">Logout</a>'.format(
        #                 current_user.name, current_user.email, current_user.profile_pic_url
        #             )
        #         )
        return render_template("index.html")  # TODO: make it look like you are loged in
    else:
        return render_template("index.html")


@app.route("/login")
def login():

    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    login_url, state = oauth.authorization_url(authorize_url)
    session["state"] = state
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
    discord_token = OAuth2Session(
        client_id, redirect_uri=redirect_uri, state=session["state"], scope=scope
    )

    token = discord_token.fetch_token(
        token_url,
        client_secret=discordkey,
        authorization_response=request.url,
    )
    session["discord_token"] = token

    global response
    discord = OAuth2Session(client_id, token=session["discord_token"])
    response = discord.get(base_discord_api_url + "/users/@me")
    # https://discordapp.com/developers/docs/resources/user#user-object-user-structure
    if response.json()["verified"] == True:
        unique_id = response.json()["id"]
        users_email = response.json()["email"]
        picture = response.json()["avatar"]
        users_name = response.json()["username"]
        discriminator = response.json()["discriminator"]
    else:
        return "User email not available or not verified by Discord.", 400

    picture_url = get_avatar + unique_id + "/" + picture

    user = User(
        id_=unique_id,
        name=users_name,
        discriminator=discriminator,
        email=users_email,
        profile_pic_url=picture_url,
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, discriminator, users_email, picture_url)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect("/")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


########################## API #################################


def add_solution(username: str, challenge_id: int, code: str):
    """Adds the given information to the database"""
    db = SQLite3DatabaseHandler("./solutions.db")
    db.connect()
    db.create_table(challenge_id)
    db.insert_values(challenge_id, username, code)


def get_challenge_solution_data(number):
    data = {"ok": True, "solutions": {}, "error": "", "message": ""}
    try:
        solutions = db.get_values(number)
    except Exception as e:
        print(e)
        data["ok"] = False
        data["message"] = "Data not found"
        data["error"] = f"Unable to find solutions to challenge {number}"
        return jsonify(data)

    for solution in solutions:
        data["solutions"][solution[0]] = {"language": solution[1], "code": solution[2]}

    data["ok"] = bool(data["solutions"])

    if not data["ok"]:
        data["message"] = "No Data for the challenge"
        data["error"] = f"No data in the database for the challenge {number}"

    return data


@app.get("/api/solutions/<int:number>")
def get_challenge_sollution(number):
    if (
        request.headers.get("API-KEY") == os.environ["PROBE_API_KEY"]
        and request.headers.get("User-Agent") == "probe-cli"
    ):
        return jsonify(get_challenge_solution_data(number))

    else:
        return jsonify(
            {
                "ok": False,
                "message": "Access denied",
                "error": "Unable to recognize the User-Agent, check the API key",
                "solutions": {},
            }
        )


@app.post("/api/solutions/submit")
def submit():
    data = request.json
    if not data:
        return jsonify(
            {
                "ok": False,
                "message": "No data provided",
                "error": "JSON data not found.",
            }
        )

    if any(key not in data for key in ["username", "language", "code"]):
        return jsonify(
            {
                "ok": False,
                "message": "Missing data",
                "error": "Missing data in the JSON data, check the keys",
            }
        )

    if request.headers.get("API-KEY") == session["discord_token"]["access_token"]:
        add_solution(data["username"], data["language"], data["code"])
        return jsonify({"ok": True, "message": "Solution submitted"})
    else:
        return jsonify(
            {
                "ok": False,
                "message": "Access denied",
                "error": "Unable to recognize the API key",
            }
        )


@app.errorhandler(404)
def page_not_found(error):  # TODO: better error handelling needed
    return jsonify({"response_code": 404})


@app.errorhandler(400)
def no_data(error):  # TODO: better error handelling needed
    return jsonify({"response_code": 400, "status": "NO data"})


@app.errorhandler(500)
def internal_server_error(error):  # TODO: better error handelling needed
    return jsonify({"response_code": 500, "status": "NO data"})
    # return render_template('tabbed.html')


if __name__ == "__main__":
    app.run(
        debug=os.getenv("DEBUG") == "true",
        use_reloader=False,
        host="0.0.0.0",
        port=5000,
    )

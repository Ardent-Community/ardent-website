from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('tabbed.html')

@app.route("/login")
def login():
    pass


if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG")=="true", use_reloader=False, host='0.0.0.0', port=5000)


from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
	return render_template('tabbed.html')

# @app.route('/docs')
# def docs():
#     return render_template('test.html')

if __name__=='__main__':
	app.run(debug=True, port=8000)

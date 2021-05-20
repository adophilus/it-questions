from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def homeView ():
	return render_template("current/home.html")

if (__name__ == "__main__"):
	app.run(debug = True)
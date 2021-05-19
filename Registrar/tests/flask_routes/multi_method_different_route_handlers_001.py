from flask import Flask

app = Flask(__name__)

@app.route("/get")
def getRequest ():
	return "[GET] response"

@app.route("/get", methods = [ "POST" ])
def postRequest ():
	return "[POST] response"

if __name__ == "__main__":
	app.run(host = "localhost", port = 2000, debug = True)
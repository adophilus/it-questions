from flask_sqlalchemy import SQLAlchemy
from flask import abort
from flask import Flask
from flask import request

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///on_the_fly_database_001.db"
db = SQLAlchemy(app)

@app.route("/create-table", methods = [ "GET", "POST" ])
def createTable ():
	creator = str(request.form.get("creator"))
	table_name = str(request.form.get("table_name"))
	if (not table_name):
		abort(404)
		return
	customTable = db.Table(table_name, db.metadata,
		db.Column("id", db.Integer, primary_key = True),
		db.Column("creator", db.String(100)),
		db.Column("table_name", db.String(100))
	)
	db.metadata.create_all(db.engine)
	print(customTable)
	return str(customTable)

app.run(debug = True, port = 2000)
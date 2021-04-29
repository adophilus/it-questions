from flask_sqlalchemy import SQLAlchemy
from flask import abort
from flask import Flask
from flask import request

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///on_the_fly_database_002.db"
db = SQLAlchemy(app)

def saveData (filename, data):
	with open(filename, "w") as fh:
		fh.write(data)

class CustomTable (db.Model):
	__tablename__ = "CustomTable"

	id = db.Column(db.Integer, autoincrement = True, primary_key = True)
	creator = db.Column(db.String(100))
	table_name = db.Column(db.String(100))

	def __init__ (self, table_name, creator):
		self.table_name = table_name
		self.creator = creator
		self.__tablename__ = table_name

	def __str__ (self):
		return self.__repr__()

	def __repr__ (self):
		return f"<CustomTable id=\"{self.id}\" table_name=\"{self.table_name}\" creator=\"{self.creator}\">"

	def setTableName (self, table_name):
		self.__tablename__ = table_name

	@classmethod
	def getAll (cls):
		return cls.query.all()

@app.route("/create-table", methods = [ "GET", "POST" ])
def createTable ():
	creator = str(request.form.get("creator"))
	table_name = str(request.form.get("table_name"))
	if (not table_name):
		abort(404)
		return
	customTable = CustomTable(table_name[0:100], creator[0:100])
	customTable.setTableName(table_name)
	# help(customTable.metadata)
	saveData("file.txt", str(dir(customTable)))
	customTable.metadata.bind = db.engine
	customTable.metadata.create_all()
	db.session.add(customTable)
	db.session.commit()
	print(customTable)
	return str(customTable)

@app.route("/get-table-data", methods = [ "GET", "POST" ])
def getTableData ():
	table_name = request.form.get("table_name")
	return str(CustomTable.getAll())

app.run(debug = True, port = 2000)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database_models_database_004.db"
db = SQLAlchemy(app)

class Test ():
	id = db.Column(db.Integer, autoincrement = True, primary_key = True)
	value = db.Column(db.String(100))

	def __init__ (self, value):
		self.value = value

class Test2 ():
	id = db.Column(db.Integer, autoincrement = True, primary_key = True)
	value = db.Column(db.String(100))

	def __init__ (self, value):
		self.value = value

testTable = db.Table("test", db.metadata,
	db.Column("id", db.Integer, autoincrement = True, primary_key = True),
	db.Column("value", db.String(100))
)

testTable.create(db.engine, True)
db.mapper(Test, testTable)
db.mapper(Test2, testTable)

db.session.add(Test("test"))
db.session.add(Test2("test2"))
db.session.commit()
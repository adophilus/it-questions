from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database_types_database_002.db"
db = SQLAlchemy(app)

class Test ():
	value = True

	def __init__ (self, value = True):
		self.value = value

testTable = db.Table("test", db.metadata,
	db.Column("id", db.Integer, autoincrement = True, primary_key = True),
	db.Column("value", db.Boolean, default = False)
)

testTable.create(db.engine, True)
db.mapper(Test, testTable)

db.session.add(Test(value = False))
db.session.add(Test(value = True))
db.session.commit()
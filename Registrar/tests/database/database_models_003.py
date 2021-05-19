from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class TestTable (db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)

testRecord = TestTable()
print(testRecord)
print(testRecord.is_active)

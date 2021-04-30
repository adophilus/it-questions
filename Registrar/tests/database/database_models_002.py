from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class Model (db.Model):
    __tablename__ = "test"
    
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String(100))

db.Table("random_table", db.metadata,
    db.Column("id", db.Integer, autoincrement = True, primary_key = True),
    db.Column("name", db.String(100))
).create(db.engine, True)

Model.__tablename__ = "random_table"
model = Model(name = "Test")
print(Model.query.all())
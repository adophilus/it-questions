from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app, engine_options = {"echo": True})

db.Table("test", db.metadata,
    db.Column("id", db.Integer, autoincrement = True),
    db.Column("name", db.String(100))
)
db.metadata.create_all(db.engine)
for key, value in db.get_binds().items():
    # print(key, value)
    help(key)
# help(db)
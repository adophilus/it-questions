
from flask import Flask
from flask_sqlalchemy import sqlalchemy, SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)


print(sqlalchemy.exc.InvalidRequestError)
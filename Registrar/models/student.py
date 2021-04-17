from flask import globals
from flask_login import UserMixin

class Student (UserMixin, globals.db.Model):
    id = globals.db.Column(globals.db.Text, primary_key = True)
    FIRST_NAME = globals.db.Column(globals.db.Text)
    LAST_NAME = globals.db.Column(globals.db.Text)
    OTHER_NAMES = globals.db.Column(globals.db.Text)
    AGE = globals.db.Column(globals.db.Integer)
    USERNAME = globals.db.Column(globals.db.Text)
    PASSWORD = globals.db.Column(globals.db.Text)
    EMAIL = globals.db.Column(globals.db.Text)
    PHONE_NUMBER = globals.db.Column(globals.db.Text)
    BIRTHDAY = globals.db.Column(globals.db.Date)
    DEPARTMENT = globals.db.Column(globals.db.Text)
    ACCOUNT_STATUS = globals.db.Column(globals.db.Text)
    ACCOUNT_TYPE = globals.db.Column(globals.db.Text)

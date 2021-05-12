from flask import globals
from flask_login import UserMixin

from ..controllers.config import config

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
    DEPARTMENT = globals.db.Column(globals.db.Text, nullable = False)
    ACCOUNT_TYPE = globals.db.Column(globals.db.Text, default = config.getAccountType("student")["name"])
    ACCOUNT_STATUS = globals.db.Column(globals.db.Text, default = config.getAccountStatus("ACTIVE"))

    def __bool__ (self):
        return True

    @classmethod
    def getByEmail (cls, email):
        return cls.query.filter_by(EMAIL = email).first()

    @classmethod
    def getById (cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def getByUsername (cls, username):
        return cls.query.filter_by(USERNAME = username).first()
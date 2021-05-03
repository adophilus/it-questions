from flask import globals
from flask_login import UserMixin
from flask_sqlalchemy import Model

class SchoolCalendar (UserMixin, globals.db.Model):
    DAY = globals.db.Column(globals.db.Float, primary_key = True)
    DAY_TYPE = globals.db.Column(globals.db.Text)
    ACTIVITY = globals.db.Column(globals.db.Text)
    BROADCAST = globals.db.Column(globals.db.Boolean)

    @classmethod
    def getById (cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def getAll (cls):
        return cls.query.all()
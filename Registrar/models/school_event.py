from flask import globals
from flask_login import UserMixin
from flask_sqlalchemy import Model

class SchoolEvent (UserMixin, globals.db.Model):
    id = globals.db.Column(globals.db.Text, primary_key = True)
    DAY = globals.db.Column(globals.db.Date)
    EVENT = globals.db.Column(globals.db.Text)
    DESCRIPTION = globals.db.Column(globals.db.Text)
    VENUE = globals.db.Column(globals.db.Text)

from flask import globals
from flask_login import UserMixin

class SchoolCalendar (UserMixin, globals.db.Model):
    DAY = globals.db.Column(globals.db.Float, primary_key = True)
    DAY_TYPE = globals.db.Column(globals.db.Text)
    ACTIVITY = globals.db.Column(globals.db.Text)
    BROADCAST = globals.db.Column(globals.db.Boolean)

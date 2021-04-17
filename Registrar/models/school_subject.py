from flask import globals
from flask_login import UserMixin

class SchoolSubject (UserMixin, globals.db.Model):
    VARIABLE_NAME = globals.db.Column(globals.db.Text, primary_key = True)
    SUBJECT_NAME = globals.db.Column(globals.db.Text)
    SUBJECT_TEACHERS = globals.db.Column(globals.db.Text)
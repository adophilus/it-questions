from flask import globals
from flask_login import UserMixin

class Chatroom (UserMixin, globals.db.Model):
    id = globals.db.Column(globals.db.Text, primary_key = True)
    NAME = globals.db.Column(globals.db.Text)
    MEMBERS = globals.db.Column(globals.db.Text)

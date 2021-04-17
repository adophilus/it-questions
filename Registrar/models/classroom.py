from flask import globals
from flask_login import UserMixin

class Classroom (UserMixin, globals.db.Model):
    id = globals.db.Column(globals.db.Text, primary_key = True)
    NAME = globals.db.Column(globals.db.Text)
    MEMBERS = globals.db.Column(globals.db.Text)
    # CHATROOMS = globals.db.Column(globals.db.Text)
    IMAGE_PATH = globals.db.Column(globals.db.Text, default = "/static/media/classroom-default.png")
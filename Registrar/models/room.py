from datetime import datetime
from flask import globals
from flask_sqlalchemy import Model
class Room (globals.db.Model):
	id = globals.db.Column(globals.db.Text, primary_key = True)
	NAME = globals.db.Column(globals.db.String(100), nullable = False)
	TYPE = globals.db.Column(globals.db.String(32), default = globals.config["room"]["type"]["classroom"]["hash"], nullable = False)
	MEMBERS = globals.db.Column(globals.db.Text, default = "{}", nullable = False)
	CONTACT_AREA = globals.db.Column(globals.db.String(globals.config["id_length"]["contact_area"] * globals.config["id_per_level"]["classroom"]), default = "")
	IMAGE_PATH = globals.db.Column(globals.db.Text, default = "/static/media/classroom-default.png")

class RoomContactArea ():
	id = globals.db.Column(globals.db.Integer, autoincrement = True)
	TYPE = globals.db.Column(globals.db.String(32), default = globals.config["contact_area"]["message"]["type"]["message"]["hash"])
	MESSAGE = globals.db.Column(globals.db.String(65000), nullable = False)
	SENDER = globals.db.Column(globals.db.String(globals.config["id_length"]["account"]), nullable = False)
	DATE_SENT = globals.db.Column(globals.db.DateTime, default = datetime.utcnow)

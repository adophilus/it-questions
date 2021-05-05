from datetime import datetime
from flask import globals
from flask_sqlalchemy import Model

from ..controllers.config import config

class Room (globals.db.Model):
	id = globals.db.Column(globals.db.Text, primary_key = True)
	NAME = globals.db.Column(globals.db.String(100), nullable = True, unique = True)
	TYPE = globals.db.Column(globals.db.String(32), default = config["room"]["type"]["classroom"]["hash"], nullable = False)
	MEMBERS = globals.db.Column(globals.db.Text, default = "{}", nullable = False)
	CONTACT_AREA = globals.db.Column(globals.db.String(config["id_length"]["contact_area"] * config["id_per_level"]["classroom"]), default = "")
	IMAGE_PATH = globals.db.Column(globals.db.Text, default = "/static/media/classroom-default.png")

class RoomContactArea ():
	id = globals.db.Column(globals.db.Integer, autoincrement = True)
	TYPE = globals.db.Column(globals.db.String(32), default = config["contact_area"]["message"]["type"]["message"]["hash"])
	MESSAGE = globals.db.Column(globals.db.String(65000), default = config["contact_area"]["message"]["type"]["message"]["hash"], nullable = False)
	SENDER = globals.db.Column(globals.db.String(config["id_length"]["account"]), nullable = False)
	DATE_SENT = globals.db.Column(globals.db.DateTime, default = datetime.utcnow)

	def __init__ (self, TYPE = TYPE, MESSAGE = MESSAGE, SENDER = SENDER):
		self.TYPE = TYPE
		self.MESSAGE = MESSAGE
		self.SENDER = SENDER
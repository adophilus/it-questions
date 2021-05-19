from flask import globals

from ..controllers.config import config
from ..controllers.private_key_generator import PrivateKeyGenerator

class SchoolEvent (globals.db.Model):
	generator = PrivateKeyGenerator()

	id = globals.db.Column(globals.db.String(config["id_length"]["school_event"]), primary_key = True)
	DATE_TIME = globals.db.Column(globals.db.DateTime)
	EVENT = globals.db.Column(globals.db.String(200))
	DESCRIPTION = globals.db.Column(globals.db.Text)
	VENUE = globals.db.Column(globals.db.String(100))

	def __init__ (self, DATE_TIME = DATE_TIME, EVENT = EVENT, DESCRIPTION = DESCRIPTION, VENUE = VENUE):
		self.id = self.__generateId__()
		self.DATE_TIME = DATE_TIME
		self.EVENT = EVENT
		self.DESCRIPTION = DESCRIPTION
		self.VENUE = VENUE

	def __iter__ (self):
		return [
			[ "id", self.id ],
			[ "datetime", self.DATE_TIME.strftime("%d/%m/%Y %H:%M") ],
			[ "event", self.EVENT ],
			[ "description", self.DESCRIPTION ],
			[ "venue", self.VENUE ]
		].__iter__()

	@classmethod
	def __generateId__ (cls, unique = True):
		while True:
			id = cls.generator.generate(level = config["id_length"]["school_event"])

			if (unique):
				schoolEvent = cls.getById(id)

				if (not schoolEvent):
					return id

	def as_dict (self):
		return dict(self.__iter__())

	@classmethod
	def getById (cls, id):
		return cls.query.filter_by(id = id).first()

	@classmethod
	def getAll (cls):
		return cls.query.all()

	def add (self):
		globals.db.session.add(self)
		globals.db.session.commit()

	def remove (self):
		globals.db.session.remove(self)
		globals.db.session.commit()
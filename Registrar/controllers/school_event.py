from flask import globals

from .private_key_generator import PrivateKeyGenerator
from .. import models

class SchoolEvent ():
	__exists__ = False
	generator = PrivateKeyGenerator()

	def __init__ (self, TITLE, id = None, DATE = None, EVENT = None, DESCRIPTION = None):
		self.schoolEvent = models.SchoolEvent.getById(id)
		self.__exists__ = True

		if (not self.schoolEvent):
			self.__exists__ = False
			self.schoolEvent = models.SchoolEvent(
				id = models.SchoolEvent.__generateId__(),
				TITLE = TITLE
			)

			if (DATE):
				self.schoolEvent.DATE = DATE
			if (EVENT):
				self.schoolEvent.EVENT = EVENT
			if (DESCRIPTION):
				self.schoolEvent.DESCRIPTION = DESCRIPTION

	@classmethod
	def __generateId__ (cls, unique = True):
		while True:
			id = self.generator.generate(level = globals.config["id_length"]["school_event"])

			if (unique):
				schoolEvent = models.SchoolEvent.getById(id)

				if not (schoolEvent):
					return id

	def get (self, field):
		return self.schoolEvent[field]

	def set (self, field, value):
		self.schholEvent[field] = value

	def create (self):
		if (not self.__exists__):
			globals.db.session.add(self.schoolEvent)
			globals.db.session.commit()
			self.__exists__ = True

	def delete (self):
		if (self.__exists__):
			globals.db.session.delete(self.schoolEvent)
			globals.db.session.commit()
			self.__exists__ = False
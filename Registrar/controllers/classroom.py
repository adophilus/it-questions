from datetime import datetime
from flask import globals

from .config import config
from .methods import jsonize, unjsonize
from .private_key_generator import PrivateKeyGenerator
from ..models import Room, RoomContactArea

class ClassroomInvalidFieldException (Exception):
	def __init__ (self, field, invalid_type = None, expected_type = None):
		self.message = f"Invalid field {field} was attempted to be set"
		if (invalid_type and expected_type):
			self.message = f"Got {invalid_type} when expecting {expected_type}"

	def __bool__ (self):
		return False

class Classroom ():
	__exists__ = False
	generator = PrivateKeyGenerator()
	members = {}

	def __init__ (self, classroom_id = "", classroom_name = None, contact_area = None, classroom_members = None, image_path = None):
		classroom = Classroom.getById(classroom_id)

		if (classroom):
			self.__exists__ = True
			self.contactArea = ClassroomContactArea(classroom_id = classroom.CONTACT_AREA)
			self.members = unjsonize(classroom.MEMBERS)
			if (classroom_name):
				classroom.NAME = classroom_name
			if (contact_area):
				self.contactArea = contact_area
				classroom.CONTACT_AREA = contact_area.classroom_id
			if (classroom_members):
				self.addMember(*classroom_members)
			if (image_path):
				classroom.IMAGE_PATH = image_path
		else:
			classroom = Room(id = Classroom.__generateId__(), NAME = classroom_name, IMAGE_PATH = image_path)
			self.contactArea = ClassroomContactArea(classroom_id = classroom.id)
			classroom.CONTACT_AREA = self.contactArea.classroom_id
			self.members = {}
			if (contact_area):
				self.contactArea = contact_area
				classroom.CONTACT_AREA = contactArea.classroom_id
			if (classroom_members):
				self.addMember(*classroom_members)
			if (image_path):
				classroom.IMAGE_PATH = self.IMAGE_PATH

		classroom.TYPE = config["room"]["type"]["classroom"]["hash"]
		self.classroom = classroom

	def __dict__ (self):
		return self.id

	def __str__ (self):
		return self.id

	@classmethod
	def __generateId__ (cls, unique = True):
		while True:
			id = cls.generator.generate(level = config["id_length"]["classroom"])

			if (unique):
				classroom = Classroom.getById(id)

				if not (classroom):
					return id

	@classmethod
	def getById (cls, classroom_id):
		return Room.query.filter_by(id = classroom_id).first()

	@classmethod
	def getByName (cls, name):
		return Room.query.filter_by(NAME = name).first()

	@classmethod
	def getStatus (cls, status_name):
		return config.getClassroomStatus(status_name)

	def addMember (self, *members, status = "AWAITING_VERIFICATION"):
		status = Classroom.getStatus(status)
		added_members = []
		for member in members:
			if (not member.id in self.members.keys()):
				classroom_profile = {
					member.id: {
						"ACCOUNT_TYPE": member.accountType,
						"ACCOUNT_STATUS": member.get("ACCOUNT_STATUS"),
						"status": config.getClassroomStatus(status)
					}
				}
				self.members.update(classroom_profile)
				added_members.append(member)
				member.addClassroom(self, classroom_profile)
		self.classroom.MEMBERS = jsonize(self.members)
		globals.db.session.commit()
		return added_members

	def hasMember (self, member):
		return member.get("id") in self.members.keys()

	def removeMember (self, *members):
		removed_members = []
		for member in members:
			if (not self.hasMember(member)):
				continue
			del self.classroom.members[member.id]
			removed_members.append(member)
		globals.db.session.commit()
		return removed_members

	def get (self, field):
		if (field == "id"):
			return self.classroom.id
		if (field == "NAME"):
			return self.classroom.NAME
		elif (field == "TYPE"):
			return self.classroom.TYPE
		elif (field == "CONTACT_AREA"):
			return self.contactArea
		elif (field == "IMAGE_PATH"):
			return self.classroom.IMAGE_PATH
		else:
			raise ClassroomInvalidFieldException(field)

	def set (self, field, value):
		if (field == "NAME"):
			self.classroom.NAME = value
		elif (field == "TYPE"):
			self.classroom.TYPE = value
		elif (field == "CONTACT_AREA"):
			if (not isinstance(value, ClassroomContactArea)):
				raise ClassroomInvalidFieldException(field)
			self.contactArea = value
			self.classroom.CONTACT_AREA = value.classroom_id
		elif (field == "IMAGE_PATH"):
			self.classroom.IMAGE_PATH = value
		else:
			raise ClassroomInvalidFieldException(field)

	def create (self):
		if (not self.__exists__):
			globals.db.session.add(self.classroom)
			globals.db.session.commit()
			self.contactArea.create()
			self.__exists__ = True

	def delete (self):
		if (self.__exists__):
			self.contactArea.drop(globals.db.engine, True)
			globals.db.session.delete(self.classroom)
			globals.db.session.commit()
			self.__exists__ = False

	def getMessages (self):
		return self.contactArea.getMessages()

	def addMessage (self, sender_id, message, message_type = config["contact_area"]["message"]["type"]["message"]["hash"]):
		return self.contactArea.addMessage(sender_id, message, message_type)

class ClassroomMessage ():
	def __init__ (self, queryResult):
		self.id = queryResult.id
		self.TYPE = queryResult.TYPE
		self.MESSAGE = queryResult.MESSAGE
		self.SENDER = queryResult.SENDER
		self.DATE_SENT = queryResult.DATE_SENT

	def __dict__ (self):
		return f"classroom_{self.id}"

class ClassroomContactArea ():
	__exists__ = False

	def __init__ (self, classroom_id, table_prefix = "room_"):
		self.classroom_id = classroom_id
		self.table = globals.db.Table(f"{table_prefix}{self.classroom_id}", globals.db.metadata,
			globals.db.Column("id", globals.db.Integer, autoincrement = True, primary_key = True),
			globals.db.Column("TYPE", globals.db.String(32), default = config["contact_area"]["message"]["type"]["message"]["hash"]),
			globals.db.Column("MESSAGE", globals.db.String(65000), default = config["contact_area"]["message"]["type"]["message"]["hash"], nullable = False),
			globals.db.Column("SENDER", globals.db.String(config["id_length"]["account"]), nullable = False),
			globals.db.Column("DATE_SENT", globals.db.DateTime, default = datetime.utcnow),
			extend_existing = True
		)

		self.__exists__ = self.table.exists(globals.db.engine)

	def create (self):
		if (not self.__exists__):
			self.table.create(globals.db.engine, True)
			globals.db.mapper(RoomContactArea, self.table)
			self.__exists__ = True

	def drop (self, bind = None, checkfirst = False):
		self.table.drop(bind, checkfirst)
		self.__exists__ = False

	def getMessages (self):
		if (self.__exists__):
			return [ClassroomMessage(message) for message in globals.db.session.query(self.table).all()]
		else:
			return []

	def addMessage (self, sender_id, message, message_type = config["contact_area"]["message"]["type"]["message"]["hash"]):
		record = RoomContactArea(
			TYPE = message_type,
			MESSAGE = message,
			SENDER = sender_id
		)

		globals.db.session.add(record)
		globals.db.session.commit()
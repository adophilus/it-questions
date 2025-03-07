from datetime import datetime
from flask import globals
from flask_sqlalchemy import sqlalchemy

from .config import config
from .methods import printDebug, jsonize, unjsonize
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
	members_to_add = []

	def __init__ (self, classroom_id = "", classroom_name = None, contact_area = None, classroom_members = None, image_path = None, _object = None, check = False):
		if (_object):
			classroom = _object
		elif (classroom_id):
			classroom = Room.getById(classroom_id)
		elif (classroom_name):
			classroom = Room.getByName(classroom_name)
		else:
			classroom = Room.getById(classroom_id)

		if (classroom):
			self.__exists__ = True
			printDebug(f"classroom ({classroom_id}) exists", "Classroom")
			self.contactArea = ClassroomContactArea(classroom_id = classroom.CONTACT_AREA)
			self.members = unjsonize(classroom.MEMBERS)
			if (classroom_name):
				classroom.NAME = classroom_name
			if (contact_area):
				self.contactArea = contact_area
				self.contactArea.create()
				classroom.CONTACT_AREA = contact_area.classroom_id
			if (classroom_members):
				self.addMember(*classroom_members)
			if (image_path):
				classroom.IMAGE_PATH = image_path
			classroom.TYPE = config["room"]["type"]["classroom"]["hash"]
			self.classroom = classroom
		elif (check):
			pass
		else:
			# printDebug(f"classroom ({classroom_id}) does not exist", "Classroom")
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

		# printDebug(f"classroom {self} has been instantiatiated", "Classroom")

	def __dict__ (self):
		return self.id

	def __bool__ (self):
		return self.__exists__

	def __str__ (self):
		return self.get("id")

	def __repr__ (self):
		return "<Classroom id='" + self.get("id") +"'>"

	def __iter__ (self):
		return [
			[ "id", self.get("id") ],
			[ "name", self.get("NAME") ],
			[ "type", "classroom" ],
			[ "image", self.get("IMAGE_PATH") ]
		].__iter__()

	def as_dict (self):
		return dict(self.__iter__())

	@classmethod
	def __generateId__ (cls, unique = True):
		while True:
			id = cls.generator.generate(level = config["id_length"]["classroom"])

			if (unique):
				classroom = Classroom(classroom_id = id, check = True)

				if not (classroom):
					return id

	@classmethod
	def getAll (cls):
		return [ Classroom(_object = room) for room in Room.getAll() ]

	@classmethod
	def getById (cls, classroom_id):
		return cls(classroom_id = classroom_id)

	@classmethod
	def getByName (cls, classroom_name):
		return cls(classroom_name = classroom_name)

	@classmethod
	def getStatus (cls, status_name):
		return config.getClassroomStatus(status_name)

	def addMember (self, *members, status = "AWAITING_CLEARANCE", nobypass = True):
		if (not (self.__exists__ or nobypass)):
			for member in members:
				self.members_to_add.append([ member, status ])
			return [ False for _ in range(len(members)) ]

		status = Classroom.getStatus(status)["status"]
		added_members = []
		for member in members:
			if (not member.get("id") in self.members.keys()):
				classroom_profile = {
					member.get("id"): {
						"ACCOUNT_TYPE": member.accountType,
						"ACCOUNT_STATUS": member.get("ACCOUNT_STATUS"),
						"status": status
					}
				}
				self.members.update(classroom_profile)
				member.addClassroom(self, classroom_profile)
				added_members.append(member)
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
			del self.classroom.members[member.get("id")]
			removed_members.append(member)
		globals.db.session.commit()
		return removed_members

	def get (self, field):
		if (str(field).lower() == "id"):
			return self.classroom.id
		if (str(field).upper() == "NAME"):
			return self.classroom.NAME
		elif (str(field).upper() == "TYPE"):
			return self.classroom.TYPE
		elif (str(field).upper() == "CONTACT_AREA"):
			return self.contactArea
		elif (str(field).upper() == "IMAGE_PATH"):
			return self.classroom.IMAGE_PATH
		else:
			raise ClassroomInvalidFieldException(field)

	def set (self, field, value):
		if (str(field).upper() == "NAME"):
			self.classroom.NAME = value
		elif (str(field).upper() == "TYPE"):
			self.classroom.TYPE = value
		elif (str(field).upper() == "CONTACT_AREA"):
			if (not isinstance(value, ClassroomContactArea)):
				raise ClassroomInvalidFieldException(field)
			self.contactArea = value
			self.classroom.CONTACT_AREA = value.classroom_id
		elif (str(field).upper() == "IMAGE_PATH"):
			self.classroom.IMAGE_PATH = value
		else:
			raise ClassroomInvalidFieldException(field)

	def create (self):
		if (not self.__exists__):
			if (len(self.members_to_add) > 0):
				for i in range(len(self.members_to_add)):
					member = self.members_to_add.pop(0)
					self.addMember(member[0], status = member[1], nobypass = True)
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

	def deleteMessage (self, message):
		if (isinstance(message, str)):
			message = self.contactArea.getMessageById(message)
		elif (isinstance(message, ClassroomMessage)):
			pass
		else:
			raise Exception(f"Invalid classroom message {message}")

		return self.contactArea.deleteMessage(message)

class ClassroomMessage ():
	def __init__ (self, queryResult):
		self.id = queryResult.id
		self.TYPE = queryResult.TYPE
		self.MESSAGE = queryResult.MESSAGE
		self.SENDER = queryResult.SENDER
		self.DATE_SENT = queryResult.DATE_SENT

	def __iter__ (self):
		return [
			[ "id", self.id ],
			[ "type", self.TYPE ],
			[ "message", self.MESSAGE ],
			[ "sender", self.SENDER ],
			[ "date_sent", self.DATE_SENT.strftime("%d/%m/%Y %H:%M") ]
		].__iter__()

	def as_dict (self):
		return dict(self.__iter__())

class ClassroomContactArea ():
	__exists__ = False

	def __init__ (self, classroom_id, table_prefix = "room_"):
		self.classroom_id = classroom_id
		self.table_name = f"{table_prefix}{self.classroom_id}"
		self.table = globals.db.Table(self.table_name, globals.db.metadata,
			globals.db.Column("id", globals.db.Integer, autoincrement = True, primary_key = True),
			globals.db.Column("TYPE", globals.db.String(32), default = config["contact_area"]["message"]["type"]["message"]["hash"]),
			globals.db.Column("MESSAGE", globals.db.String(65000), default = config["contact_area"]["message"]["type"]["message"]["hash"], nullable = False),
			globals.db.Column("SENDER", globals.db.String(config["id_length"]["account"]), nullable = False),
			globals.db.Column("DATE_SENT", globals.db.DateTime, default = datetime.utcnow),
			extend_existing = True
		)

		self.__exists__ = self.table.exists(globals.db.engine)
		# printDebug(f"checking if the table ({self}) already exists ({self.__exists__})", "ClassroomContactArea")
		if (self):
			# printDebug(f"table already exists, mapping...", "ClassroomContactArea")
			self.mapTable()

	def __repr__ (self):
		return f"<ClassroomContactArea table_name='{self.table_name}' of='{self.classroom_id}'>"

	def __bool__ (self):
		return self.__exists__

	def create (self):
		if (not self.__exists__):
			self.table.create(globals.db.engine, True)
			self.mapTable()
			self.__exists__ = True

	def drop (self, bind = None, checkfirst = False):
		self.table.drop(bind, checkfirst)
		self.__exists__ = False

	def mapTable (self):
		# printDebug(f"mapping table {self}", "ClassroomContactArea.mapTable")
		try:
			return globals.db.mapper(RoomContactArea, self.table)
		except sqlalchemy.exc.ArgumentError:
			return globals.db.mapper(RoomContactArea, self.table, non_primary = True)

	def deleteMessage (self, message):
		try:
			globals.db.session.delete(message)
			globals.db.session.commit()
			return True
		except Exception as e:
			printDebug(e, "ClassroomContactArea.deleteMessage")
			return False

	def getMessageById (self, message_id):
		return globals.db.session.query(self.table).filter_by(id = message_id).first()

	def getMessages (self):
		if (self.__exists__):
			return [ ClassroomMessage(message) for message in globals.db.session.query(self.table).all() ]
		return []

	def addMessage (self, sender_id, message, message_type = config["contact_area"]["message"]["type"]["message"]["hash"]):
		record = RoomContactArea(
			TYPE = message_type,
			MESSAGE = message,
			SENDER = sender_id
		)

		globals.db.session.add(record)
		globals.db.session.commit()
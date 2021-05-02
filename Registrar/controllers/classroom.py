from datetime import datetime
from flask import globals

from . import config, method
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

	def __init__ (self, classroom_id = "", classroom_name = None, contact_area_id = None, classroom_members = None, image_path = None):
		classroom = Classroom.getById(classroom_id)
		if (classroom):
			self.__exists__ = True
			self.id = classroom.id
			self.NAME = classroom.NAME
			self.CONTACT_AREA = ClassroomContactArea(classroom_id = classroom.CONTACT_AREA)
			self.IMAGE_PATH = classroom.IMAGE_PATH
			if (classroom_name):
				self.NAME = classroom_name
				classroom.NAME = self.NAME
			if (classroom_members):
				self.addMember(*classroom_members)
			if (contact_area_id):
				self.CONTACT_AREA = ClassroomContactArea(classroom_id = contact_area_id)
				classroom.CONTACT_AREA = contact_area_id
			if (image_path):
				classroom.IMAGE_PATH = image_path
				self.IMAGE_PATH = image_path
			self.classroom = classroom
		else:
			self.id = Classroom.__generateId__()
			self.NAME = classroom_name
			self.CONTACT_AREA = ClassroomContactArea(classroom_id = ClassroomContactArea.__generateId__())
			classroom = Room(id = self.id, NAME = self.NAME)
			if (classroom_members):
				self.addMember(*classroom_members)
			if (contact_area_id):
				self.CONTACT_AREA = ClassroomContactArea(classroom_id = contact_area_id)
				classroom.CONTACT_AREA = contact_area_id
			else:
				self.CONTACT_AREA = ClassroomContactArea(classroom_id = self.id)
				classroom.CONTACT_AREA = self.id
			if (image_path):
				self.IMAGE_PATH = image_path
				classroom.IMAGE_PATH = self.IMAGE_PATH
			else:
				self.IMAGE_PATH = classroom.IMAGE_PATH
			self.classroom = classroom

	@classmethod
	def __generateId__ (cls, unique = True):
		while True:
			id = globals.IDgenerator.generate(level = globals.config["id_length"]["classroom"])

			if (unique):
				classroom = Classroom.getById(id)

				if not (classroom):
					return id

	@classmethod
	def getById (cls, classroom_id):
		return Room.query.filter_by(id = classroom_id).first()

	@classmethod
	def getStatus (cls, status_name):
		return config.getClassroomStatus(status_name)

	def addMember (self, *members, status = "AWAITING_CLEARANCE"):
		status = Classroom.getStatus(status)
		added_members = []
		for member in members:
			classroom_members = globals.controller.method.unjsonize(self.classroom.MEMBERS)
			if (not member.id in classroom_members.keys()):
				classroom_profile = {
					member.id: {
						"ACCOUNT_TYPE": member.ACCOUNT_TYPE,
						"ACCOUNT_STATUS": member.ACCOUNT_STATUS,
						"status": status
					}
				}
				classroom_members.update(classroom_profile)
				added_members.append(member.id)
		self.classroom.MEMBERS = controller.method.jsonize(classroom_members)
		return added_members

	def set (self, field, value):
		if (field == "NAME"):
			self.NAME = value
		elif (field == "TYPE"):
			self.TYPE = value
			self.classroom.TYPE = value
		elif (field == "CONTACT_AREA"):
			self.CONTACT_AREA = value.classroom_id
			self.classroom.CONTACT_AREA = value.classroom_id
		elif (field == "IMAGE_PATH"):
			self.IMAGE_PATH = value
			self.classroom.IMAGE_PATH = value
		else:
			raise ClassroomInvalidFieldException(field)

	def create (self):
		if (not self.__exists__):
			self.CONTACT_AREA.create()
			globals.db.session.add(self.classroom)
			globals.db.session.commit()
			self.__exists__ = True

	def delete (self):
		if (self.__exists__):
			self.CONTACT_AREA.drop(globals.db.engine, True)
			globals.db.session.delete(self.classroom)
			globals.db.session.commit()
			self.__exists__ = False

	def getMessages (self):
		return self.CONTACT_AREA.getMessages()

class ClassroomContactArea ():
	__exists__ = False

	def __init__ (self, classroom_id, table_prefix = "room_"):
		self.classroom_id = classroom_id
		self.table = globals.db.Table(f"{table_prefix}{self.classroom_id}", globals.db.metadata,
			globals.db.Column("id", globals.db.Integer, autoincrement = True),
			globals.db.Column("TYPE", globals.db.String(32), default = globals.config["contact_area"]["message"]["type"]["message"]["hash"]),
			globals.db.Column("MESSAGE", globals.db.String(65000), nullable = False),
			globals.db.Column("SENDER", globals.db.String(globals.config["id_length"]["account"]), nullable = False),
			globals.db.Column("DATE_SENT", globals.db.DateTime, default = datetime.utcnow),
			extend_existing = True
		)

		self.__exists__ = self.table.exists(globals.db.engine)

	def create (self):
		if (not self.__exists__):
			self.table.create(globals.db.engine, True)
			globals.db.mapper(RoomContactArea, self.table)
			self.contactArea = RoomContactArea()
			self.__exists__ = True

	def getMessages (self):
		if (self.__exists__):
			return globals.db.session.query(self.table).all()
		else:
			return []
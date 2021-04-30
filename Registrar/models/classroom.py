from flask import globals
from flask_login import UserMixin

class ClassroomModel (UserMixin, globals.db.Model):
	id = globals.db.Column(globals.db.Text, primary_key = True)
	NAME = globals.db.Column(globals.db.Text, nullable = False)
	MEMBERS = globals.db.Column(globals.db.Text, default = "{}", nullable = False)
	CLASSROOM = globals.db.Column(globals.db.String(globals.config["id_length"]["classroom"] * globals.config["id_per_level"]["classroom"]), default = "")
	IMAGE_PATH = globals.db.Column(globals.db.Text, default = "/static/media/classroom-default.png")

class Classroom ():
	__exists__ = False

	def __init__ (self, classroom_id, classroom_name = None, classroom_room = None, members = None, image_path = None):
		classroom = ClassroomModel.getById(classroom_id)
		if (classroom):
			self.__exists__ = True
			self.id = classroom.id
			self.NAME = classroom.name
			self.CLASSROOM = ClassroomMessage(id = classroom.CLASSROOM)
			self.IMAGE_PATH = classroom.IMAGE_PATH
			if (classroom_name):
				self.NAME = classroom_name
				classroom.NAME = self.NAME
			if (classroom_members):
				self.MEMBERS = classroom_members
				classroom.MEMBERS = self.MEMBERS
			if (classroom_room):
				self.CLASSROOM = ClassroomMessage(id = classroom_room)
				classroom.CLASSROOM = self.CLASSROOM
			if (image_path):
				classroom.IMAGE_PATH = image_path
				self.IMAGE_PATH = image_path
			self.classroom = classroom
		else:
			self.id = Classroom.__generateId__()
			self.NAME = classroom_name
			self.CLASSROOM = ClassroomMessage(id = ClassroomMessage.__generateId__())
			classroom = ClassroomModel(id = self.id, NAME = self.NAME, CLASSROOM = self.Classroom)
			if (classroom_members):
				self.MEMBERS = classroom_members
				classroom.MEMBERS = self.MEMBERS
			if (classroom_room):
				self.CLASSROOM = ClassroomMessage(id = classroom_room)
				classroom.CLASSROOM = self.CLASSROOM
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
				classroom = globals.methods.getClassroomById(id)

				if not (classroom):
					return id

	@classmethod
	def getById (cls, classroom_id):
		return ClassroomModel.query.filter_by(id = classrom_id).first()

	def create (self):
		if (not self.__exists__):
			self.CLASSROOM.create()
			globals.db.session.add(self.classroom)
			globals.db.session.commit()
			self.__exists__ = True

	def delete (self):
		if (self.__exists__):
			self.CLASSROOM.drop(globals.db.engine, True)
			globals.db.session.delete(self.classroom)
			globals.db.session.commit()
			self.__exists__ = False

class ClassroomMessage ():
	__exists__ = False

	def __init__ (self, classroom_id):
		pass

	@classmethod
	def __generateId__ (cls, unique = True):
		while True:
			id = globals.IDgenerator.generate(level = globals.config["id_length"]["classroom"])

			if (unique):
				classroom = globals.methods.getClassroomById(id)

				if not (classroom):
					return id

	def create (self):
		globals.db.Table(f"classroom_{self.classroom.id}", globals.db.metadata,
			globals.db.Column("id", globals.db.Integer, autoincrement = True),
			globals.db.Column("TYPE", globals.db.String(32), default = globals.config["classroom"]["messages"]["types"]["message"]["hash"]),
			globals.db.Column("MESSAGE", globals.db.String(65000), nullable = False),
			globals.db.Column("DATE_SENT", globals.db.DateTime)
		).create(globals.db.engine, True)
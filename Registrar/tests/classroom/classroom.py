from flask import globals

from ...controllers import Classroom

def createClassroom ():
	classroom = Classroom(classroom_name = "SS3")
	classroom.create()

def checkClassroomMessages ():
	classroom = Classroom(classroom_id = "wNjKAp7LPPgaJFmrmN9Z")
	print(type(classroom.CONTACT_AREA.getMessages()))
	print(type(classroom.CONTACT_AREA.getMessages()[0]))
	print(type(classroom.CONTACT_AREA.getMessages()[0].id))
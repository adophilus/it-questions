from flask import globals

def createClassroom ():
	classroom = globals.model.Classroom(classroom_name = "SS3")
	classroom.create()

def checkClassroomMessages ():
	classroom = globals.model.Classroom(classroom_id = "wNjKAp7LPPgaJFmrmN9Z")
	print(classroom.CONTACT_AREA.getMessages())
from datetime import datetime
from flask import globals
from time import sleep

from ...controllers import Classroom

def createClassroom ():
	classroom = Classroom(classroom_name = "SS3")
	classroom.create()
	return classroom

def checkClassroomMessages (classroom):
	# print(type(classroom.CONTACT_AREA.getMessages()))
	# print(type(classroom.CONTACT_AREA.getMessages()[0]))
	# print(type(classroom.CONTACT_AREA.getMessages()[0].id))
	print(classroom.getMessages())

def runClassroomTests ():
	classroom1 = createClassroom()
	# classroom2 = createClassroom()

	classroom1.addMessage("prPAMrUtzq5ChiVqillCvJxN8", f"The date right now is {datetime.now()}")
	checkClassroomMessages(classroom1)
	sleep(10)
	classroom1.delete()
	# classroom2.addMessage("prPAMrUtzq5ChiVqillCvJxN8", f"The date right now is {datetime.now()}")
	# checkClassroomMessages(classroom2)
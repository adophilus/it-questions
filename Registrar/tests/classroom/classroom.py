from flask import globals

def createClassroom ():
	classroom = globals.model.Classroom(classroom_name = "SS3")
	classroom.create()
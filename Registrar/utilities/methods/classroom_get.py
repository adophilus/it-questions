from flask import globals
import os

def _getClassroomByName (class_name):
    classroom = globals.model.Classroom.query.filter_by(NAME = class_name)

    if (classroom.first()):
        return classroom

def getClassroomByName (class_name):
    classroom = _getClassroomByName(class_name)
    if (classroom):
        return [classroom.first()]

def getClassroomDetails (classroom_id):
	try:
		classroom_details = globals.General.loadJson(os.path.join("data", "classroom", classroom_id, "details.json"))
		return classroom_details
	except FileNotFoundError:
		return None

def _getClassroomById (id):
    classroom = globals.model.Classroom.query.filter_by(id = id)

    if (classroom.first()):
        return classroom

def getClassroomById (id):
    classroom = _getClassroomById(id)
    if (classroom):
        return classroom.first()

def getClassroomDict (classroom):
    if (not classroom):
        return classroom

    return {
        "id": classroom.id,
        "NAME": classroom.NAME,
        "MEMBERS": globals.General.jsonize(classroom.MEMBERS),
        "IMAGE_PATH": classroom.IMAGE_PATH
    }

def getClassroomStatus (classroom_status):
    if (not globals.config["classroom"]["statuses"].get(classroom_status)):
        return False

    return globals.config["classroom"]["statuses"][classroom_status].get("status")
from flask import globals
from flask_login import current_user

def generateClassroomId (unique = False):
	while True:
		id = globals.IDgenerator.generate(level = globals.config["id_length"]["classroom"])

		if (unique):
			classroom = globals.methods.getClassroomById(id)

			if not (classroom):
				return id

def createClassroom (classroom_name, commit = False):
	classroom_id = generateClassroomId(True)
	classroom =  globals.Classroom(
		id = classroom_id,
		NAME = classroom_name,
		MEMBERS = globals.General.unjsonize({})
	)
	globals.db.session.add(classroom)
	if (commit):
		globals.db.session.commit()
	return classroom

def deleteClassroom (classroom_id, commit = False):
	classroom = globals.methods.getClassroomById(classroom_id)
	if (not classroom):
		return False
	
	globals.db.session.delete(classroom)

	if (commit):
		globals.db.session.commit()
	return True

def addUserToClassroom (user, classroom, commit = False):
	classroom_profile = {
		user.id: {
			"ACCOUNT_TYPE": user.ACCOUNT_TYPE,
			"ACCOUNT_STATUS": user.ACCOUNT_STATUS,
			"status": globals.methods.getClassroomStatus("AWAITING_CLEARANCE")
		}
	}

	classroom_members = globals.General.jsonize(classroom.MEMBERS)
	if (user.id in classroom_members.keys()):
		return False

	classroom_members.update(classroom_profile)
	classroom.MEMBERS = globals.General.unjsonize(classroom_members)
	if (commit):
		globals.db.session.commit()
	return {
		classroom.id: classroom_profile[user.id]
	}

def removeUserAccountFromClassroom (account, classroom, commit = False):
	user_id = account.id

	if not (globals.methods.User(account = account).isStudent() or globals.methods.User(account = account).isTeacher()):
		return False

	classroom_id = account_details["classroom"]["id"]

	classroom = getClassroomById(classroom_id)

	classroom_members = globals.General.jsonize(classroom.MEMBERS)

	if (user_id in classroom_members.keys()):
		del classroom_members[user_id]
	else:
		return False

	classroom.MEMBERS = globals.General.json.dumps(classroom_members)

	if (commit):
		globals.db.session.commit()
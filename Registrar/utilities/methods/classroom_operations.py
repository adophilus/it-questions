from flask import globals
from flask_login import current_user

def createClassroom (classroom_name, classroom_members = {}, classroom_image = None):
	classroom_id = generateClassroomId(True)

	classroomMessagesTable = globals.db.Table(f"classroom_{classroom_id}", globals.db.metadata,
		globals.db.Column("id", globals.db.Integer, autoincrement = True),
		globals.db.Column("TYPE", globals.db.String(32), default = globals.config["classroom"]["messages"]["type"]["message"]["hash"]),
		globals.db.Column("MESSAGE", globals.db.String(65000), nullable = False),
		globals.db.Column("DATE_SENT", globals.db.DateTime)
	)
	globals.db.metadata.create_all(globals.db.engine)

	classroom =  globals.model.Classroom(
		id = classroom_id,
		NAME = classroom_name,
		MEMBERS = globals.General.unjsonize(classroom_members),
		CLASSROOM = f"classroom_{classroom_id}"
	)

	if (classroom_image):
		classrom.IMAGE_PATH = classroom_image

	globals.db.session.add(classroom)
	globals.db.session.commit()

	return classroom

def deleteClassroom (classroom_id, commit = False):
	classroom = globals.model.Classroom.getById(classroom_id)
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

def removeUserAccountFromClassroom (account, classroom_id, commit = False):
	user_id = account.get("id")

	if not (globals.methods.User(account = account).isStudent() or globals.methods.User(account = account).isTeacher()):
		return False

	classroom = getClassroomById(classroom_id)

	classroom_members = globals.General.jsonize(classroom.MEMBERS)

	if (user_id in classroom_members.keys()):
		del classroom_members[user_id]
	else:
		return False

	classroom.MEMBERS = globals.General.json.dumps(classroom_members)

	if (commit):
		globals.db.session.commit()
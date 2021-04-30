from flask import Blueprint
from flask import globals
from flask import redirect
from flask import url_for
from flask_login import current_user, login_required

development = Blueprint("dev", __name__)

@development.route("/get-id")
def getId ():
	if (current_user.is_active):
		return globals.General.sendTrue(current_user.id)
	return globals.General.sendFalse(globals.config.getMessage("LOGIN_REQUIRED"))

@development.route("/is-logged-in")
def isLoggedIn ():
	if (current_user.is_active):
		return "true"
	else:
		return "false"

@development.route("/get-account-by-id/<id>")
def getAccountById (id):
	account = globals.methods.getAccountById(id)
	if (account):
		account_details = {
			"id": account.id,
			"username": account.USERNAME,
			"password": account.PASSWORD,
			"email": account.EMAIL,
			"phone_number": account.PHONE_NUMBER,
			"birthday": globals.methods.dateToString(account.BIRTHDAY),
			"account_status": account.ACCOUNT_STATUS,
		}
		return globals.General.sendTrue(account_details)
	return globals.General.sendFalse(globals.config.getMessage("INEXISTENT_ACCOUNT"))

@development.route("/check-classroom/<classroom_id>")
def checkClassroom (classroom_id):
	classroom = globals.methods.getClassroomById(classroom_id)
	if (not classroom):
		return globals.General.sendFalse(globals.config.getMessage("INEXISTENT_CLASS"))
	return globals.General.sendTrue({"id": classroom.id, "name": classroom.NAME})

@development.route("/create-classroom/<classroom_name>")
def createClassroom (classroom_name):
	globals.methods.createClassroom(classroom_name)
	return globals.General.sendTrue(globals.config.getMessage("CLASS_CREATED"))

@development.route("/delete-classroom/<classroom_id>")
def deleteClassroom (classroom_id):
	if (globals.methods.deleteClassroom(classroom_id, commit = True)):
		return globals.General.sendTrue(globals.config.getMessage("CLASS_DELETED"))
	return globals.General.sendTrue(globals.config.getMessage("INEXISTENT_CLASS"))

@development.route("/classrooms-list")
def getClassroomsList ():
	return globals.General.sendTrue([{"id": classroom.id, "name": classroom.NAME} for classroom in globals.Classroom.query.all()])
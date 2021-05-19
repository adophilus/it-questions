from flask import Blueprint
from flask import globals
from flask import redirect
from flask import request
from flask import url_for
from flask_login import current_user, login_required

from ..controllers.account import Account
from ..controllers.config import config
from ..controllers.classroom import Classroom
from ..controllers.methods import sendFalse, sendTrue

development = Blueprint("dev", __name__)

@development.route("/get-id")
def getId ():
	if (current_user.is_active):
		return sendTrue(current_user.id)
	return sendFalse(config.getMessage("LOGIN_REQUIRED"))

@development.route("/is-logged-in")
def isLoggedIn ():
	return str(current_user.is_active).lower()

@development.route("/delete-account-by-id", methods = [ "POST" ])
def deleteAccountById ():
	account = Account(id = request.form.get("id"))
	account.delete()
	return str(account)

@development.route("/get-account-by-id/<id>")
def getAccountById (id):
	account = Account(id)
	if (account):
		account_details = {
			"id": account.get("id"),
			"username": account.get("USERNAME"),
			"password": account.get("PASSWORD"),
			"email": account.get("EMAIL"),
			"phone_number": account.get("PHONE_NUMBER"),
			"birthday": globals.methods.dateToString(account.get("BIRTHDAY")),
			"account_status": account.ACCOUNT_STATUS,
		}
		return globals.General.sendTrue(account_details)
	return globals.General.sendFalse(config.getMessage("INEXISTENT_ACCOUNT"))

@development.route("/check-classroom/<classroom_id>")
def checkClassroom (classroom_id):
	classroom = globals.model.Classroom.getById(classroom_id)
	if (not classroom):
		return globals.General.sendFalse(config.getMessage("INEXISTENT_CLASS"))
	return globals.General.sendTrue({"id": classroom.id, "name": classroom.NAME})

@development.route("/create-classroom/<classroom_name>")
def createClassroom (classroom_name):
	globals.methods.createClassroom(classroom_name)
	return globals.General.sendTrue(config.getMessage("CLASS_CREATED"))

@development.route("/delete-classroom/<classroom_id>")
def deleteClassroom (classroom_id):
	if (globals.methods.deleteClassroom(classroom_id, commit = True)):
		return globals.General.sendTrue(config.getMessage("CLASS_DELETED"))
	return globals.General.sendTrue(config.getMessage("INEXISTENT_CLASS"))

@development.route("/classroom/<classroom_id>/message")
def getClassroomMessages (classroom_id):
	if (not classroom_id):
		classroom_id = "XTbDgBtkXQrIKa825XkR"
	classroom = Classroom(classroom_id = classroom_id)
	return sendTrue([ message.as_dict() for message in classroom.getMessages() ])
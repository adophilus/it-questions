from flask import Blueprint
from flask import globals
from flask_login import current_user, login_required
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from ..controllers.config import config
from ..controllers.classroom import Classroom
from ..controllers.methods import printDebug, sendFalse, sendTrue

classroom = Blueprint("classroom", __name__)

@classroom.route("/")
@login_required
def classroomIndexPage ():
	account = current_user
	classrooms = account.getClassrooms()

	return render_template(f"{account.accountType}/classroom.html",
		no_of_unread_public_remarks = 0,
		no_of_unread_notifications = 0,
		no_of_unseen_results = 0,
		account = account,
		classrooms = classrooms)


@classroom.route("/<classroom_id>/message")
@login_required
def getClassroomMessages (classroom_id):
	account = current_user
	classroom = Classroom(classroom_id = classroom_id)

	printDebug(f"classroom: {classroom}", "ClassroomBlueprint.getClassroomMessages")
	printDebug(f"classroom.__bool__(): {bool(classroom)}", "ClassroomBlueprint.getClassroomMessages")
	printDebug(f"classroom_id: {classroom_id}", "ClassroomBlueprint.getClassroomMessages")
	if (not classroom):
		return sendFalse(config.getMessage("INEXISTENT_CLASSROOM"))

	if (not classroom.hasMember(account)):
		return sendFalse(config.getMessage("ACCESS_DENIED"))

	return sendTrue([ message.as_dict() for message in classroom.getMessages() ])

@classroom.route("/<classroom_id>/message", methods = [ "PUT" ])
@login_required
def putClassroomMessage (classroom_id):
	account = current_user
	classroom = Classroom(classroom_id = classroom_id)
	message = request.form.get("message")

	if (not classroom):
		return sendFalse(config.getMessage("INEXISTENT_CLASSROOM"))

	if (not classroom.hasMember(account)):
		return sendFalse(config.getMessage("ACCESS_DENIED"))

	classroom.addMessage(current_user.id, message)
	return sendTrue(config.getMessage("CLASS_MESSAGE_SENT"))
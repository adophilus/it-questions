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
def classroomView ():
	account = current_user
	classrooms = account.getClassrooms()

	return render_template(f"{account.accountType}/classroom.html",
		no_of_unread_public_remarks = 0,
		no_of_unread_notifications = 0,
		no_of_unseen_results = 0,
		account = account,
		classrooms = classrooms)

@classroom.route("/list")
def getClassroomsList ():
	return sendTrue([ classroom.as_dict() for classroom in Classroom.getAll() ])

@classroom.route("/<classroom_id>/message")
@login_required
def getClassroomMessages (classroom_id):
	account = current_user
	classroom = Classroom(classroom_id = classroom_id)

	if (not classroom):
		return sendFalse(config.getMessage("INEXISTENT_CLASSROOMROOM"))

	if (not classroom.hasMember(account)):
		return sendFalse(config.getMessage("ACCESS_DENIED"))

	return sendTrue([ message.as_dict() for message in classroom.getMessages() ])

@classroom.route("/<classroom_id>/message/<message_id>")
@login_required
def getClassroomMessagesAfter (classroom_id, message_id):
	account = current_user
	classroom = Classroom(classroom_id = classroom_id)

	if (not classroom):
		return sendFalse(config.getMessage("INEXISTENT_CLASSROOMROOM"))

	if (not classroom.hasMember(account)):
		return sendFalse(config.getMessage("ACCESS_DENIED"))


	n = False
	messages = classroom.getMessages()
	for x in range(len(messages)):
		if (n != False):
			x = x - n

		if (str(messages[x].id) == message_id):
			n = x + 1
			messages[:n] = [ ]
			continue

		if (not n):
			messages[x] = messages[x].as_dict()
			continue

		if (x < 0):
			break

		messages[x] = messages[x].as_dict()
	return sendTrue(messages)

@classroom.route("/<classroom_id>/message", methods = [ "PUT" ])
@login_required
def putClassroomMessage (classroom_id):
	account = current_user
	classroom = Classroom(classroom_id = classroom_id)
	message = request.form.get("message")

	if (not classroom):
		return sendFalse(config.getMessage("INEXISTENT_CLASSROOMROOM"))

	if (not classroom.hasMember(account)):
		return sendFalse(config.getMessage("ACCESS_DENIED"))

	classroom.addMessage(current_user.id, message)
	return sendTrue(config.getMessage("CLASSROOM_MESSAGE_SENT"))

@classroom.route("/<classroom_id>/message", methods = [ "DELETE" ])
@login_required
def deleteClassroomMessage (classroom_id):
	account = current_user
	classroom = Classroom(classroom_id = classroom_id)
	message_id = request.form.get("message_id")

	if (not classroom):
		return sendFalse(config.getMessage("INEXISTENT_CLASSROOMROOM"))

	if (not classroom.hasMember(account)):
		return sendFalse(config.getMessage("ACCESS_DENIED"))

	message = classroom.getMessageById(message_id)
	if (not message):
		return sendFalse(config.getMessage("INEXISTENT_CLASSROOM_MESSAGE"))

	if (classroom.deleteMessage(message)):
		return sendTrue(config.getMessage("CLASSROOM_MESSAGE_DELETED"))
	return sendFalse(config.getMessage("CLASSROOM_MESSAGE_NOT_DELETED"))
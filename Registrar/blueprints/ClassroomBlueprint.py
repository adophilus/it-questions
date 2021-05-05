from flask import Blueprint
from flask import globals
from flask_login import current_user, login_required
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for

from ..controllers import Account, config, Classroom
from ..controllers.methods import sendFalse, sendTrue

classroom = Blueprint("classroom", __name__)

@classroom.route("/")
@login_required
def classroomIndexPage ():
	account = Account(_object = current_user)
	classrooms = []

	if (account.isStudent() or account.isTeacher()):
		classrooms = account.classrooms

	return render_template("classroom/classroom.html",
		no_of_unread_public_remarks = 0,
		no_of_unread_notifications = 0,
		no_of_unseen_results = 0,
		Account = account,
		classrooms = classrooms)


@classroom.route("/list", methods = [ "GET", "POST" ])
def getClassroomsList ():
	return sendFalse("Not implemented yet")

@classroom.route("/<classroom_id>/message/get")
@login_required
def getClassroomMessages (classroom_id):
	account = Account(_object = current_user)
	classroom = Classroom(classroom_id = classroom_id)

	if (not classroom.__exists__):
		return sendFalse(config.getMessage("INEXISTENT_CLASSROOM"))

	if (not classroom.hasMember(account)):
		return sendFalse(config.getMessage("ACCESS_DENIED"))

	return sendTrue(classroom.getMessages())
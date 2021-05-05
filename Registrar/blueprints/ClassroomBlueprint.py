from flask import Blueprint
from flask import globals
from flask_login import current_user, login_required
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for

from ..controllers import Account, config, Classroom, Client
from ..controllers.method import sendFalse, sendTrue

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


@classroom.route("/list", methods = [ "POST" ])
@login_required
def getClassroomsList ():
	return sendFalse("Not implemented yet")

@classroom.route("/<classroom_id>/message/get")
@login_required
def getClassroomMessages (classroom_id):
	classroom = Classroom(classroom_id = classroom_id)

	if (not classroom.__exists__):
		return sendFalse(config.getMessage("INEXISTENT_CLASSROOM"))

	if (classroom.hasMember(current_user.id) or Client.isStudent()):
		return sendTrue(classroom.getMessages())

	return sendFalse(config.getMessage("ACCESS_DENIED"))
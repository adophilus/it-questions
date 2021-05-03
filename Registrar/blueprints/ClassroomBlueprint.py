from flask import Blueprint
from flask import globals
from flask_login import current_user, login_required
from flask import redirect
from flask import session
from flask import url_for

from ..controllers import config, Classroom, Client
from ..controllers.method import sendFalse, sendTrue

classroom = Blueprint("classroom", __name__)

@classroom.route("/")
@login_required
def classroomIndexPage ():
	return globals.methods.renderClassroomPage()

@classroom.route("/list", methods = [ "POST" ])
@login_required
def getClassroomsList ():
	return sendFalse("Not implemented yet")

@classroom.route("/<classroom_id>/message/get")
@login_required
def getClassroomMessages (classroom_id):
	if (classroom.hasMember(current_user.id) or Client.isStudent()):
		classroom = Classroom(classroom_id)
		if (not classroom.__exists__):
			return sendFalse(config.getMessage("INEXISTENT_CLASSROOM"))
		return sendTrue(classroom.getMessages())
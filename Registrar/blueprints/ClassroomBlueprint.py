from flask import Blueprint
from flask import globals
from flask_login import current_user, login_required
from flask import redirect
from flask import session
from flask import url_for

classroom = Blueprint("classroom", __name__)

@classroom.route("/")
@login_required
def classroomIndexPage ():
	return globals.methods.renderClassroomPage()

@classroom.route("/<id>")
@login_required
def subClassroomPage (id):
	subClassroom = globals.getSubClassroomById(id)
	if (subClassroom):
		return "true"
	return globals.General.sendFalse(globals.config.getMessage("INEXISTENT_CLASSROOM"))
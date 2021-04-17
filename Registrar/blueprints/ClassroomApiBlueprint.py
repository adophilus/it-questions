from flask import Blueprint
from flask import globals
from flask_login import current_user, login_required
from flask import redirect
from flask import session
from flask import url_for

classroomApi = Blueprint("classroomApi", __name__)

@classroomApi.route("/list", methods = ["POST"])
@login_required
def getClassroomsList ():
	if (globals.methods.Client.isStudent() or globals.methods.Client.isTeacher()):
		account_details = globals.methods.getAccountDetails(None, globals.methods.getAccountBySession())
		return globals.General.sendTrue([globals.methods.getClassroomDict(globals.methods.getClassroomById(classroom_id)) for classroom_id in account_details["classroom"].keys()])
	return globals.General.sendTrue([])
from flask import globals
from flask import make_response
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user, logout_user
from pprint import pprint

def renderClassroomPage ():
	account_details = globals.methods.getAccountDetails(current_user.id, current_user)
	pprint(account_details)
	return render_template("classroom/classroom.html",
		Account = current_user,
		no_of_unread_public_remarks = 0,
		no_of_unread_notifications = 0,
		no_of_unseen_results = 0,
		Client = globals.methods.Client,
		account_details = account_details,
		getClassroomById = globals.model.Classroom.getById,
		# no_of_classrooms = len(account_details)
		classroom = account_details["classroom"]) #globals.methods.getClassrooms())

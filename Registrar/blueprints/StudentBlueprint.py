from datetime import datetime
from flask import Blueprint
from flask import globals
from flask import make_response
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask_login import login_required, current_user

from ..controllers import calendar
from ..controllers.account import Account
from ..controllers.methods import sendTrue

from .MainBlueprint import mainLoginPage

import os

student = Blueprint("student", __name__)

@student.route("/")
@login_required
def homeView ():
	account = Account(_object = current_user)
	if (not account.isStudent()):
		return redirect(url_for(f"{account.accountType}.homeView"))

	return render_template(f"{account.accountType}/home.html", account = account, url_for = url_for, date_and_time = calendar.getDateTime(), weeks = calendar.getCalendarArray(), no_of_unread_notifications = 0)

@student.route("classroom/list", methods = [ "POST" ])
@login_required
def getClassroomsList ():
	account = Account(_object = current_user)
	return sendTrue([ classroom.as_dict() for classroom in account.getClassrooms() ])

@student.route("/logout")
@login_required
def studentLogoutPage ():
	account = Account(_object = current_user)
	if (not account.isStudent()):
		return redirect(f"/{account.get('ACCOUNT_TYPE')}")

	return redirect(url_for("handler.handleLogout"))

@student.route("/<id>")
@login_required
def lookupStudentByIdPage (id):
	return sendFalse("not implemented yet!")

	# return render_template(
	#     "profile.html",
	#     Account = account,
	#     account_description = globals.methods.getAccountDetails(account.get("id")).get("description"),
	#     date_and_time = date_and_time
	# )

	# studentCookie = {
	#     "search_query": {
	#         "type": "ID",
	#         "value": id
	#     },
	#     "result": []
	# }

	# if (id in globals.model.Students.selectColumn("ID")):
	#     # I used "students" here rather than "student". Although IDs are unique and no two students (or any two acccounts) can have the same ID, I felt its safer to just loop though all the students matching a particular ID.
	#     students = globals.model.Students.select({
	#         "where": {
	#             "ID": id
	#         }
	#     })

	#     i = 0
	#     for row in students:
	#         studentCookie["result"].append({
	#             "index": i,
	#             "first_name": student["column"]["FIRST_NAME"],
	#             "last_name": student["column"]["LAST_NAME"]
	#         })
	#         i += 1

	# response = make_response(f"Welcome Student {id}")
	# response.set_cookie("student", unjsonize(studentCookie))

	# return response

# @student.route("/first name:<first_name>")
# @student.route("/first-name:<first_name>")
# @student.route("/first_name:<first_name>")
def lookupStudentByFirstNamePage (firstName):
	checkStudent()
	studentCookie = {
		"search_query": {
			"type": "FIRST_NAME",
			"value": firstName
		},
		"result": []
	}

	if (firstName in globals.model.Students.selectColumn("FIRST_NAME")):
		students = globals.model.Students.select({
			"where": {
				"FIRST_NAME": firstName
			}
		})

		i = 0
		for row in students:
			studentCookie["result"].append({
				"index": i,
				"first_name": student["column"]["FIRST_NAME"],
				"last_name": student["column"]["LAST_NAME"]
			})
			i += 1

	response = make_response(f"Welcome Student {id}")
	response.set_cookie("student", unjsonize(studentCookie))

	return response

@student.route("/results")
@login_required
def lookupStudentResultPage ():
	account = Account(_object = current_user)
	if (not account.isStudent()):
		return redirect(f"/{account.get('ACCOUNT_TYPE')}")

	return render_template("student/results.html")
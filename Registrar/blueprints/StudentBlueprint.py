from datetime import datetime
from flask import Blueprint
from flask import globals
from flask import make_response
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask_login import login_required, current_user, logout_user
from utilities.General import *
from blueprints.MainBlueprint import mainLoginPage
import os
student = Blueprint("student", __name__)


def checkStudent ():
	if current_user.ACCOUNT_TYPE != globals.config["account"]["types"]["student"]["name"]:
		return globals.methods.redirectUserToHomePage()

@student.route("/")
@login_required
def studentIndexPage ():
	if current_user.ACCOUNT_TYPE != globals.config["account"]["types"]["student"]["name"]:
		return globals.methods.redirectUserToHomePage()

	return globals.methods.renderUserAccountHomePage()
	
@student.route("/logout")
@login_required
def studentLogoutPage ():
	if current_user.ACCOUNT_TYPE != globals.config["account"]["types"]["student"]["name"]:
		return globals.methods.redirectUserToHomePage()

	return redirect(url_for("handler.handleLogout"))

@student.route("/<id>")
@login_required
def lookupStudentByIdPage (id):
	return globals.methods.renderAccountPageOf(id, globals.STUDENT["name"])

	# return render_template(
	#     "profile.html",
	#     Account = account,
	#     account_description = globals.methods.getAccountDetails(account.id).get("description"),
	#     date_and_time = date_and_time
	# )

	# studentCookie = {
	#     "search_query": {
	#         "type": "ID",
	#         "value": id
	#     },
	#     "result": []
	# }

	# if (id in globals.students.selectColumn("ID")):
	#     # I used "students" here rather than "student". Although IDs are unique and no two students (or any two acccounts) can have the same ID, I felt its safer to just loop though all the students matching a particular ID.
	#     students = globals.students.select({
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

	if (firstName in globals.students.selectColumn("FIRST_NAME")):
		students = globals.students.select({
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
	if current_user.ACCOUNT_TYPE != globals.config["account"]["types"]["student"]["name"]:
		return globals.methods.redirectUserToHomePage()

	return render_template("student/results.html")

@student.route("/remove-account")
@login_required
def removeStudentAccount ():
	if current_user.ACCOUNT_TYPE != globals.config["account"]["types"]["student"]["name"]:
		return globals.methods.redirectUserToHomePage()

	return globals.methods.removeUserAccount(current_user.id)
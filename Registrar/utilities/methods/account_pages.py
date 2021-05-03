from flask import globals
from flask import make_response
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user, logout_user

from .account_get import *
from .account_auth import *
from .question_get import *

import calendar
import datetime
import urllib

def renderInexistentAccountPage ():
	message = globals.General.unjsonize({
		"account_search_code": 404,
		"message": globals.config.getMessage("INEXISTENT_ACCOUNT_SEARCH")
	})

	cookie_data = {
		"key": "account_search",
		"value": urllib.parse.quote(message),
		"path": f"/{current_user.ACCOUNT_TYPE}"
	}

	return renderUserAccountHomePage([cookie_data])

def renderUserAccountHomePage (cookies = []):
	try:
		dt = datetime.datetime.now()
		date_and_time = {
			"date": dt.strftime("%d"),
			"day": globals.months[int(dt.strftime("%m"))],
			"month": globals.months[int(dt.strftime("%m"))],
			"year": dt.strftime("%Y")
		}

		account_details = getAccountDetails(current_user.id)
		if (globals.config["account"]["statuses"][account_details["status"]].get("grant_access")):
			keys = {
				"Account": current_user,
				"account_details": account_details,
				"Client": Client,
				"date_and_time": date_and_time,
				"no_of_unread_notifications": 0,
				"weeks": getCalendarArray(),
			}

			if (Client.isAdmin()):
				keys["questions_list"] = account_details.get("questions")
				keys["questions_list_length"] = len(keys["questions_list"])
				keys["getQuestionDetails"] = getQuestionDetails
			elif (Client.isTeacher()):
				keys["questions_list"] = account_details.get("questions")
				keys["questions_list_length"] = len(keys["questions_list"])
				keys["getQuestionDetails"] = getQuestionDetails

				# print(keys["questions_list"][0]["id"],
				# 		keys["questions_list"][0]["type"])
				# print("\n\n\n\n",
				# 	getQuestionDetails(
				# 		keys["questions_list"][0]["id"],
				# 		keys["questions_list"][0]["type"]
				# 	),
				# 	"\n\n\n\n")

			elif (Client.isStudent()):
				keys["no_of_unread_public_remarks"] = 0
				keys["no_of_unseen_results"] = 0

			response = make_response(render_template("account/home.html", **keys))

			for cookie in cookies:
				response.set_cookie(**cookie)
			return response

		logout_user()
		return redirect("main.mainLoginPage")
	except FileNotFoundError:
		logout_user()
		return redirect("main.mainLoginPage")

def renderAccountPageOf (id, account_type):
	is_admin = Client.isAdmin()
	is_teacher = Client.isTeacher()
	is_parent = Client.isParent()
	if not (is_admin or is_teacher or is_parent):
		return globals.methods.redirectUserToHomePage()

	account = Account(id)

	if not account:
		return renderInexistentAccountPage()

	if account.ACCOUNT_TYPE != account_type:
		return renderInexistentAccountPage()

	if (is_admin):
		if (globals.methods.Client.isAdmin()):
			return render_template("administrator/display/account-details.html", Account = account)

	if (is_teacher):
		return render_template("teacher/display/account-details.html", Account = account)

	if (is_parent):
		parent_account_details = globals.methods.getAccountDetails(current_user.id)
		if id not in parent_account_details.get("wards"):
			return renderInexistentAccountPage()
		return render_template("parent/display/account-details.html", Account = account)

def getPresent ():
	return datetime.datetime.now()

def getPresentYMD ():
	present = getPresent()
	return f"{present.year}-{str(present.month).zfill(2)}-{present.day}"

def getPresentDMY ():
	present = getPresent()
	return f"{present.day}-{str(present.month).zfill(2)}-{present.year}"

def getCalendarArray ():
	present = getPresent()
	weeks = calendar.Calendar(calendar.SUNDAY).monthdatescalendar(present.year, present.month)
	nweeks = []
	number_of_days = 0
	for week in weeks:
		nweek = []
		for day in week:
			if (number_of_days == 33):
				break
			if (day.month == present.month - 1 or day.month == present.month + 1):
				nweek.append({"day": None, "today": False, "month": present.month})
			elif (day.day == present.day and day.month == present.month):
				nweek.append({"day": day.day, "today": True, "month": present.month})
			else:
				nweek.append({"day": day.day, "today": False, "month": present.month})
			number_of_days += 1
		nweeks.append(nweek)
	return nweeks

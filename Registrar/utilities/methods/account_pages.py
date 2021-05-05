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
		if (config["account"]["statuses"][account_details["status"]].get("grant_access")):
			keys = {
				"Account": account,
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

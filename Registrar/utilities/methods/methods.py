from flask import globals
from flask import render_template
from flask import redirect
from flask import session
from flask_login import logout_user, current_user

from .account_auth import *
from .account_get import *
from .account_pages import *
from .account_put import *
from .account_operations import *
# from .classroom_get import *
# from .classroom_operations import *
from .classroom_pages import *
from .database import *
from .question_get import *
from .question_operations import *
from .question_put import *
from .school_event_get import *
from .school_events import *
from .guardian_ward import *
from .user import *

class RunningProcesses ():
	def register (pid, name, description):
		record = {
			"PID": pid,
			"PROCESS_NAME": name,
			"PROCESS_DESCRIPTION": description
		}

		if not (pid):
			record["PID"] = os.getpid()

		globals.running_processes.insert(record)

	def save ():
		globals.running_processes.save()

def redirectUserToHomePage ():
	# print("\n\n\n\n", current_user, "\n\n\n\n")
	return redirect(f"/{current_user.ACCOUNT_TYPE}")


def dateToString (date):
	array = {
		"day": date.strftime("%d"),
		"month": date.strftime("%m"),
		"year": date.strftime("%Y")
	}

	array["ymd"] = f'{array["year"]}-{array["month"]}-{array["day"]}'
	return array
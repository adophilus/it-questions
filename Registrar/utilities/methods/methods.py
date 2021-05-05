from flask import globals
from flask import render_template
from flask import redirect
from flask import session
from flask_login import logout_user, current_user

from .account_pages import *
from .account_put import *
from .account_operations import *
from .question_get import *
from .question_operations import *
from .question_put import *
from .school_event_get import *
from .school_events import *
from .guardian_ward import *
from .user import *

class RunningProcesses ():
	@classmethod
	def register (cls, pid, name, description):
		record = {
			"PID": pid,
			"PROCESS_NAME": name,
			"PROCESS_DESCRIPTION": description
		}

		if not (pid):
			record["PID"] = os.getpid()

		globals.running_processes.insert(record)

	@classmethod
	def save (cls):
		globals.running_processes.save()

def redirectUserToHomePage ():
	return redirect(f"/{current_user.ACCOUNT_TYPE}")
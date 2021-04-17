from flask import Blueprint
from flask import globals
from flask import request
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

from utilities.General import *

handlerQuestion = Blueprint("handlerQuestion", __name__)

@handlerQuestion.route("/create/<question_title>")
@login_required
def createQuestion (question_title):
	if not (globals.methods.Client.isAdmin() or globals.methods.Client.isTeacher()):
		errormsg = globals.config.getMessage("UNAUTHORIZED_ACCESS")
		return globals.General.sendFalse(errormsg)
	return globals.methods.createQuestion(question_title)

@handlerQuestion.route("/list/get/mine", methods = ["GET"])
@login_required
def getUserQuestionsList ():
	if not (globals.methods.Client.isTeacher() or globals.methods.Client.isAdmin()):
		return "[]"

	user_details = globals.methods.getAccountDetails(current_user.id)
	user_questions = user_details.get("questions")
	return globals.General.unjsonize(user_questions)

@handlerQuestion.route("/details/<question_id>", methods = ["GET"])
def loadQuestionDetails (question_id):
	question = globals.methods.getQuestionById(question_id)
	if (not question):
		errmsg = globals.config.getMessage("INEXISTENT_QUESTION")
		return globals.General.unjsonize({"data": errmsg, "error": errmsg, "status": False})

	question_type = question.QUESTION_TYPE
	question_details = globals.methods.getQuestionDetails(question_id, question_type)

	if (not question_details or question_type != "public"):
		if (globals.methods.Client.isVisitor()):
			errmsg = globals.config.getMessage("QUESTION_FETCH_FAILED")
			return globals.General.unjsonize({"data": errmsg, "error": errmsg, "status": False})
		if (question.CREATOR_ID != current_user.id):
			errmsg = globals.config.getMessage("QUESTION_FETCH_FAILED")
			return globals.General.unjsonize({"data": errmsg, "error": errmsg, "status": False})

	return globals.General.unjsonize({"data": question_details, "status": True})

@handlerQuestion.route("/get/<question_id>/<question_number>", methods = ["GET"])
@login_required
def loadQuestionNumber (question_id, question_number):
	question = globals.methods.getQuestionById(question_id)
	if (not question):
		errmsg = globals.config.getMessage("INEXISTENT_QUESTION")
		return globals.General.unjsonize({"data": errmsg, "error": errmsg, "status": False})

	question_type = question.QUESTION_TYPE
	questions = globals.methods.getQuestionQuestions(question_id, question_type)
	if (not questions):
		errmsg = globals.config.getMessage("QUESTION_FETCH_FAILED")
		return globals.General.unjsonize({"data": errmsg, "error": errmsg, "status": False})

	question = questions[f"{question_number}"]
	return globals.General.unjsonize({"data": question, "status": True})


@handlerQuestion.route("/save/<question_id>/<question_number>", methods = ["POST"])
@login_required
def saveQuestionNumber (question_id, question_number):
	question = globals.methods.getQuestionById(question_id)
	question_data = globals.General.jsonize(request.form.get("question_data"))
	if (not question):
		errmsg = globals.config.getMessage("INEXISTENT_QUESTION")
		return globals.General.unjsonize({"data": errmsg, "error": errmsg, "status": False})

	question_type = question.QUESTION_TYPE

	question_details = globals.methods.getQuestionDetails(question_id, question_type)
	if (not question_details):
		errmsg = globals.config.getMessage("QUESTION_FETCH_FAILED")
		return globals.General.unjsonize({"data": errmsg, "error": errmsg, "status": False})

	questions = globals.methods.getQuestionQuestions(question_id, question_type)
	if (not questions):
		errmsg = globals.config.getMessage("QUESTION_FETCH_FAILED")
		return globals.General.unjsonize({"data": errmsg, "error": errmsg, "status": False})

	default_question_data = {
		"question": "The question goes here",
		"options": {
			"correct": [],
			"marks": 0
		}
	}

	# new_question_number = False
	# for num in range(1, int(question_number) + 1):
	# 	if not (questions.get(str(num))):
	# 		# questions[str(num)] = default_question_data
	# 		if not (new_question_number):
	# 			question_number = num

	try:
		old_marks = questions[str(question_number)]["options"].get("marks", 0)
	except KeyError:
		old_marks = 0

	questions[str(question_number)] = default_question_data
	questions[str(question_number)]["question"] = question_data["question"]

	for key in question_data["options"].keys():
		qdata = question_data["options"][str(key)]
		question_option = {
			"type": qdata["type"],
			"value": qdata["value"],
			"mark": qdata["mark"]
		}

		if (qdata["type"] == "text"):
			question_option["ignore_case"] = qdata["ignore_case"]
			question_option["match"] = qdata["match"]
		elif (qdata["type"] == "switch"):
			question_option["match"] = qdata["match"]

		questions[str(question_number)]["options"][str(key)] = question_option

		if (str(key) in question_data["correct"]):
			questions[str(question_number)]["options"]["marks"] += qdata["mark"]

	questions[str(question_number)]["options"]["correct"] = question_data["correct"]

	new_marks = questions[str(question_number)]["options"]["marks"]

	question_details["total_marks"] -= old_marks
	question_details["total_marks"] += new_marks


	# questions[str(question_number)] = question_data

	if not (globals.methods.putQuestionQuestions(question_id, questions, question)):
		errmsg = globals.config.getMessage("QUESTION_SAVE_FAILED")
		return globals.General.unjsonize({"data": errmsg, "error": errmsg, "status": False})

	question_details["last_modified"] = globals.methods.getPresentYMD()
	question_details["number_of_questions"] = len(questions.keys())
	# print("\n"*3)
	# print(questions[str(question_number)])
	# print("\n"*3)

	if not (globals.methods.putQuestionDetails(question_id, question_details, question)):
		errmsg = globals.config.getMessage("QUESTION_SAVE_FAILED")
		return globals.General.unjsonize({"data": errmsg, "error": errmsg, "status": False})

	return globals.General.unjsonize({"data": globals.config.getMessage("QUESTION_SAVE_SUCCESSFUL"), "status": True})

@handlerQuestion.route("/download/<question_id>", methods = ["GET"])
def downloadQuestionWithId (question_id):
	question = globals.methods.getQuestionById(question_id)
	if not (question):
		return globals.config.getMessage("INEXISTENT_QUESTION")
	if (globals.methods.Client.isVisitor() and question.QUESTION_TYPE != "public"):
		return globals.config.getMessage("INEXISTENT_QUESTION")
	return "Downloading question...."

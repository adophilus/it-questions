from flask import Blueprint
from flask import globals
from flask import request
from flask_login import login_required, current_user

from ..controllers.config import config

handlerQuestion = Blueprint("handlerQuestion", __name__)

@handlerQuestion.route("/create/<question_title>")
@login_required
def createQuestion (question_title):
	if not (globals.methods.Client.isAdmin() or globals.methods.Client.isTeacher()):
		errormsg = config.getMessage("UNAUTHORIZED_ACCESS")
		return globals.General.sendFalse(errormsg)
	return globals.methods.createQuestion(question_title)

@handlerQuestion.route("/list/get/mine", methods = ["GET"])
@login_required
def getUserQuestionsList ():
	if not (globals.methods.Client.isTeacher() or globals.methods.Client.isAdmin()):
		return "[]"

	user_details = globals.methods.getAccountDetails(current_user.id)
	user_questions = user_details.get("questions")
	return sendFalse(user_questions)

@handlerQuestion.route("/details/<question_id>", methods = ["GET"])
def loadQuestionDetails (question_id):
	account = Account(_object = current_user)
	question = Question(question_id = question_id)
	if (not question):
		return sendFalse(config.getMessage("INEXISTENT_QUESTION"))

	if (not question.get("IS_PUBLIC")):
		if (account.isVisitor()):
			return sendFalse(config.getMessage("QUESTION_FETCH_FAILED"))
		if (question.get("CREATOR") != account.get("id")):
			return sendFalse(config.getMessage("QUESTION_FETCH_FAILED"))

	return sendTrue(question.questionDetails)

@handlerQuestion.route("/get/<question_id>/<question_number>", methods = ["GET"])
@login_required
def loadQuestionNumber (question_id, question_number):
	question = globals.methods.getQuestionById(question_id)
	if (not question):
		return sendFalse(config.getMessage("INEXISTENT_QUESTION"))

	# question = questions[f"{question_number}"]
	return sendTrue(question)


@handlerQuestion.route("/save/<question_id>/<question_number>", methods = ["POST"])
@login_required
def saveQuestionNumber (question_id, question_number):
	question = globals.methods.getQuestionById(question_id)
	question_data = globals.General.jsonize(request.form.get("question_data"))
	if (not question):
		return sendFalse(config.getMessage("INEXISTENT_QUESTION"))

	question_type = question.QUESTION_TYPE

	question_details = globals.methods.getQuestionDetails(question_id, question_type)
	if (not question_details):
		return sendFalse(config.getMessage("QUESTION_FETCH_FAILED"))

	questions = globals.methods.getQuestionQuestions(question_id, question_type)
	if (not questions):
		return sendFalse(config.getMessage("QUESTION_FETCH_FAILED"))

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
		return sendFalse(config.getMessage("QUESTION_SAVE_FAILED"))

	question_details["last_modified"] = getPresentYMD()
	question_details["number_of_questions"] = len(questions.keys())
	# print("\n"*3)
	# print(questions[str(question_number)])
	# print("\n"*3)

	if not (globals.methods.putQuestionDetails(question_id, question_details, question)):
		return sendFalse(config.getMessage("QUESTION_SAVE_FAILED"))

	return sendFalse({"data": config.getMessage("QUESTION_SAVE_SUCCESSFUL"), "status": True})

@handlerQuestion.route("/download/<question_id>", methods = ["GET"])
def downloadQuestionWithId (question_id):
	account = Account(_object = current_user)
	question = globals.methods.getQuestionById(question_id)
	if not (question):
		return config.getMessage("INEXISTENT_QUESTION")
	if (account.isVisitor()) and (not question.get("IS_PUBLIC")):
		return config.getMessage("INEXISTENT_QUESTION")
	return "Downloading question...."

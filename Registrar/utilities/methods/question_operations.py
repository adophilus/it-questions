from flask import globals
from flask_login import current_user
from .account_auth import generateQuestionId
import os

def _getQuestionDetailsPath (question_id, question_type):
	return os.path.join("data", "questions", question_type, f"details-{question_id}.json")

def _getQuestionQuestionsPath (question_id, question_type):
	return os.path.join("data", "questions", question_type, f"question-{question_id}.json")

def createQuestion (question_title, question_type = "private"):
	creator = [ globals.methods.Client.getUsername(), globals.methods.Client.getId() ]
	date_created = globals.methods.getPresentDMY()
	question_type = question_type

	question_details = {
		"id": generateQuestionId(unique = True, question_type = question_type),
		"title": question_title,
		"creator": creator,
		"owner": creator,
		"image_path": globals.config["question"]["default_image_path"],
		"date_created": date_created,
		"number_of_questions": 1,
		"total_marks": 1,
		"last_modified": date_created
	}

	question_questions = {
		"1": {
			"question": "Question 1",
			"options": {
				"correct": [],
				"marks": 1,
				"1": {
					"type": "radio",
					"value": "Option 1",
					"mark": 1
				}
			}
		}
	}

	question = globals.Question(
		id = question_details["id"],
		QUESTION_TITLE = question_details["title"],
		QUESTION_TYPE = question_type,
		NUMBER_OF_QUESTIONS = question_details["number_of_questions"],
		CREATOR = question_details["creator"][0],
		CREATOR_ID = question_details["creator"][1],
		OWNER = question_details["owner"][0],
		OWNER_ID = question_details["owner"][1],
		IMAGE_PATH = question_details["image_path"]
	)

	account_details = globals.methods.getAccountDetails(globals.methods.Client.getId(), current_user)
	if not (account_details):
		errmsg = globals.config.getMessage("INVALID_ACCOUNT")
		return globals.General.sendFalse(errmsg)

	account_details["questions"].append({"id": question_details["id"], "type": question_type})
	has_saved_account_details = globals.methods.putAccountDetails(globals.methods.Client.getId(), account_details, current_user)
	if not (has_saved_account_details):
		errmsg = globals.config.getMessage("CHANGES_NOT_SAVED")
		return globals.General.sendFalse(errmsg)

	# globals.General.saveJson(_getQuestionDetailsPath(question_details["id"], "private"), question_details)
	# globals.General.saveJson(_getQuestionDetailsPath(question_details["id"], "private"), question_details)

	globals.methods.putQuestionDetails(question_details["id"], question_details)
	globals.methods.putQuestionQuestions(question_details["id"], question_questions)

	globals.db.session.add(question)
	globals.db.session.commit()
	return globals.General.unjsonize(question_details)

def deleteQuestionDetails (question_id, question = False):
	if not (question):
		question = globals.methods.getQuestionById(question_id)
	if not (question):
		return False
	return deleteQuestionAssetsFile(question_id, question, "details")

def deleteQuestionQuestions (question_id, question = False):
	if not (question):
		question = globals.methods.getQuestionById(question_id)
	if not (question):
		return False
	return deleteQuestionAssetsFile(question_id, question, "questions")

def deleteQuestionAssetsFile (question_id, question, asset_name = "details"):
	if not (question):
		question_type = question_id.split("-").pop(0)
	else:
		question_type = question.QUESTION_TYPE

	if (asset_name == "details"):
		return os.unlink(_getQuestionDetailsPath(question_id, question_type))
	return os.unlink(_getQuestionQuestionsPath(question_id, question_type))

def deleteQuestion (question_id, question = False):
	if not (question):
		question = globals.methods.getQuestionById(question_id)
	if not (question):
		return False

	hasDeletedQuestionDetailsFile = globals.methods.deleteQuestionDetails(question_id, question)
	hasDeletedQuestionQuestionsFile = globals.methods.deleteQuestionQuestions(question_id, question)

	status = (hasDeletedQuestionDetailsFile and hasDeletedQuestionQuestionsFile)
	if not (status):
		errmsg = globals.config.getMessage("UNSUCCESSFUL_QUESTION_DELETION")
		return globals.methods.unjsonize({"status": status, "data": errmsg, "error": errmsg})
	return globals.methods.unjsonize({"status": status, "data": globals.config.getMessage("SUCCESSFUL_QUESTION_DELETION")})

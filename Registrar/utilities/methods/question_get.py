from flask import globals
from flask import render_template
from flask_login import current_user
import os

def getQuestionDetails (question_id, question_type):
	try:
		question_details = globals.General.loadJson(os.path.join("data", "questions", question_type, f"details-{question_id}.json"))
		return question_details
	except FileNotFoundError:
		return None

def getQuestionQuestions (question_id, question_type):
	try:
		question_questions = globals.General.loadJson(os.path.join("data", "questions", question_type, f"question-{question_id}.json"))
		return question_questions
	except FileNotFoundError:
		return None

def _getQuestionById (id):
	question = globals.model.Question.query.filter_by(id = id)

	if (question.first()):
		return question

def getQuestionById (id):
	question = _getQuestionById(id)
	if (question):
		return question.first()

def getAllPublicQuestions ():
	return globals.model.Question.query.filter_by(QUESTION_TYPE = "public").all()

def renderQuestionsPoolPage ():
	return render_template("questions-pool/list.html", Client = globals.methods.Client, str = str)

def getQuestionsListAfter (question_id):
	question = getQuestionById(question_id)
	if not (question):
		questions_list = [ { "id": question.id, "title": question.QUESTION_TITLE, "image_path": question.IMAGE_PATH } for question in getAllPublicQuestions() ]
		return globals.General.unjsonize(questions_list)
	questions_list = []
	return globals.General.unjsonize(questions_list)

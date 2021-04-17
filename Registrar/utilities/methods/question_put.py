from flask import globals
import os

def _getQuestionDetailsPath (question_id, question_type):
	return os.path.join("data", "questions", question_type, f"details-{question_id}.json")

def putQuestionDetails (question_id, question_details, question = None):
	if not (question):
		question = getQuestionById(question_id)
	if not (question):
		return False

	try:
		globals.General.saveJson(_getQuestionDetailsPath(question_id, question.QUESTION_TYPE), question_details)
		return True
	except Exception as e:
		print("\n\n\n")
		print(e)
		print("\n\n\n")
		return e

def _getQuestionQuestionsPath (question_id, question_type):
	return os.path.join("data", "questions", question_type, f"question-{question_id}.json")

def putQuestionQuestions (question_id, question_questions, question = None):
	if not (question):
		question = getQuestionById(question_id)
	if not (question):
		return False

	try:
		globals.General.saveJson(_getQuestionQuestionsPath(question_id, question.QUESTION_TYPE), question_questions)
		return True
	except Exception as e:
		print("\n\n\n")
		print(e)
		print("\n\n\n")
		return e

from flask import Blueprint
from flask import globals
from flask import redirect
from flask import url_for

questionsPool = Blueprint("questions_pool", __name__)

@questionsPool.route("/")
def questionsPoolIndexPage ():
	return globals.methods.renderQuestionsPoolPage()

@questionsPool.route("/list/<question_id>")
def questionsPoolListPage (question_id):
	return globals.methods.getQuestionsListAfter(question_id)

@questionsPool.route("/<question_id>")
def displayQuesitionPage (question_id):
	return f"Displaying question data for {question_id}"

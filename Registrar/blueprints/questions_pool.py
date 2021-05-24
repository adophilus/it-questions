from flask import Blueprint
from flask import globals
from flask import redirect
from flask import url_for

from ..controllers.methods import sendFalse

questionsPool = Blueprint("questions_pool", __name__)

@questionsPool.route("/")
def questionsPoolIndexPage ():
	return sendFalse("needs revision!")

@questionsPool.route("/list/<question_id>")
def questionsPoolListPage (question_id):
	return sendFalse("not implemented yet!")

@questionsPool.route("/<question_id>")
def displayQuesitionPage (question_id):
	return f"Displaying question data for {question_id}"

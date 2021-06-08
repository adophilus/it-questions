from ...controllers.private_key_generator import PrivateKeyGenerator
from ...controllers.question import Question
from ...controllers.methods import printDebug

generator = PrivateKeyGenerator()

def createQuestionFor (account):
    question_title = generator.generate()
    question = Question(TITLE = question_title)
    question.assignOwner(account.account)
    printDebug(question)
from flask import globals
from .account_get import *
from .chatroom_message_get import *
from .question_get import *
from .school_event_get import *

def generateUserId (unique = False):
    while True:
        id = globals.IDgenerator.generate(level = globals.config["id_length"]["account"])

        if (unique):
            account = getAccountById(id)

            if not (account):
                return id

def generateQuestionId (unique = False, question_type = "private"):
    while True:
        id = globals.IDgenerator.generate(level = globals.config["id_length"]["question"])

        if (unique):
            question = getQuestionById(id)

            if not (question):
                return f"{question_type}-{id}"

def generateSchoolEventId (unique = True):
    while True:
        id = globals.IDgenerator.generate(level = globals.config["id_length"]["school-event"])

        if (unique):
            schoolEvent = getSchoolEventById(id)

            if not (schoolEvent):
                return id

def generateChatroomMessageId (chatroom_id, unique = True):
    while True:
        id = globals.IDgenerator.generate(level = globals.config["id_length"]["chatroom-message"])

        if (unique):
            chatroomMessage = getChatroomMessageById(chatroom_id, id)

            if not (chatroomMessage):
                return id

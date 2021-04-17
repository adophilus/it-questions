from flask import globals
import os

def getChatroomDetails (chatroom_id):
	try:
		chatroom_details = globals.General.loadJson(os.path.join("data", "chatroom", chatroom_id, "details.json"))
		return chatroom_details
	except FileNotFoundError:
		return None

def _getChatroomById (id):
    chatroom = globals.Chatroom.query.filter_by(id = id)

    if (chatroom.first()):
        return chatroom

def getChatroomById (id):
    chatroom = _getChatroomById(id)
    if (chatroom):
        return chatroom.first()

def getChatroomChatsPath (chatroom_id):
    path = os.path.join("data", "chatrooms", chatroom_id, "chats.csv")
    if (os.path.isfile(path)):
        return path

def loadChatrooms ():
    try:
        for key in globals.chatrooms.keys():
            globals.chatrooms[key]["chats"].save()
        for chatroom in globals.Chatroom.query.filter():
            globals.chatrooms[chatroom.id] = {
                "chats-file": getChatroomChatsPath(chatroom.id)
            }
            globals.chatrooms[chatroom.id]["chats"] = globals.CSVParser(globals.chatrooms[chatroom.id]["chats-file"], parser = globals.csvparsers.parseChatrooms, unparser = globals.csvparsers.unparseChatrooms)
    except AttributeError as e:
        globals.chatrooms = dict()
        loadChatrooms()
from flask import globals

def getChatroomMessageById (chatroom_id, id):
	chatroomParser = globals.CSVParser(globals.getChatroomChatsPath(chatroom_id))
	chatroom = chatroomParser.select({"where": {"ID": id}}, default = None)
	return chatroom
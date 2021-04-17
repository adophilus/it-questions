class Config (dict):
	def getMessage (self, message):
		return self.get("messages").get(message)
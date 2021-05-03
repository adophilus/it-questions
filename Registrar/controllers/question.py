from .private_key_generator import PrivateKeyGenerator
from .. import models

class Question ():
	__exists__ = False
	generator = PrivateKeyGenerator()

	def __init__ (self, question_id = None):
		pass

	def __bool__ (self):
		return self.__exists__

	@classmethod
	def __generateId__  (cls, unique = True, question_type = "private"):
    while True:
        id = self.generator.generate(level = config["id_length"]["question"])

        if (unique):
            question = Question(id)

            if not (question):
                return f"{question_type}-{id}"

	def create (self):
		pass

	def delete (self):
		pass
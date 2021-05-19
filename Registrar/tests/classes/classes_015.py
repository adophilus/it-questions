from json import dumps
from pprint import pprint

class Test ():
	name = "test"
	def __init__ (self, name = name):
		self.name = name

	def __dict__ (self):
		return {
			"name": self.name
		}

if __name__ == "__main__":
	t = Test()
	pprint(dumps(t))
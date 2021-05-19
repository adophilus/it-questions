from json import dumps as jsonize

class Test ():
	__name__ = "DictionarySerialization"

	def __iter__ (self):
		return [
			["name", "Test"]
		].__iter__()

	def __dict__ (self):
		return {
			"Test": {
				"name": self.__name__
			}
		}

if __name__ == "__main__":
	t = Test()
	val = { "name": "test" }
	print(jsonize(val))
	print(dict(t))

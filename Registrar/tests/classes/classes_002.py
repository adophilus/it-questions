class Test ():
	something = "default"

	def __init__ (self, something = "default"):
		self.something = something

	def doSomething (self):
		print(f"doSomething: {self.something}")

	@classmethod
	def activate (cls, something):
		return cls(something)

t = Test()
t.doSomething()
t2 = t.activate("custom_something")
t2.doSomething()
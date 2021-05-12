class SuperClass ():
	def __privateMethod (self):
		print("Private method")

	def publicMethod (self):
		self.__privateMethod()
		print("Public method")

class SubClass (SuperClass):
	pass

if __name__ == "__main__":
	sc = SuperClass()
	# generates error
	# sc.__privateMethod()
	sc.publicMethod()

	sc2 = SubClass()
	# generates error (but is inherited from superclass)
	# sc.__privateMethod()
	sc.publicMethod()
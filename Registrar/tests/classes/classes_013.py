class SuperClass (object):
	def __init__ (self):
		print("SuperClass initialized!")
		self.__privateFunc()

	def virtualFunc (self):
		print(self, "virtual function")

	def __privateFunc (self):
		print(self, "private function")

class SubClass (SuperClass):
	def __init__ (self):
		# help(super)
		super().__init__()
		print("SubClass initialized!")
		self.__privateFunc()

	def __privateFunc (self):
		print(self, "private function")

if __name__ == "__main__":
	_super = SuperClass()
	_super.virtualFunc()
	# _super.__privateFunc() # errors out
	# _super._SuperClass__privateFunc() # name mangling

	print()

	sub = SubClass()
	sub.virtualFunc()

	# sub._SubClass__privateFunc() # name mangling
	# sub.__privateFunc() # errors out
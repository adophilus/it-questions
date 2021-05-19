class Test ():
	name = ""

	def __init__ (self, name = ""):
		self.name = name

	def __bool__ (self):
		# print("kjehrufpghrpuofhrh") # gets displayed
		return bool(self.name)

if __name__ == "__main__":
	t1 = Test()
	t2 = Test("hello")

	if (t1):
		print("t1")

	if (t2):
		print("t2")
class Test ():
	exists = False

	def __repr__ (self):
		return "Class: Test"

	def __bool__ (self):
		return self.exists

if __name__ == "__main__":
	t = Test()
	print(t)
	print(bool(t))

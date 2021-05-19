class Test ():
	prop = True

	def __init__ (self, p = prop):
		print(p)
		# print(prop) # errors out

Test()
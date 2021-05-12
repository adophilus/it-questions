class Test ():
	def __init__ (self):
		self.hash_table = {}

	def __getitem__ (self, item):
		return self.hash_table[item]

	def __setitem__ (self, item, value):
		self.hash_table[item] = value

t = Test()
t[0] = "uche"
print(t[0])

# error
# print(t[2])
class Test ():
	attribute = "custom attribute"

	def getAttr (self):
		return self.attribute

	def getAttr2 (self):
		return attribute

t = Test()
print(t.attribute)
print(t.getAttr())

# errors out
# print(t.getAttr2())
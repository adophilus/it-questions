from collections import defaultdict

class Test (defaultdict):
	def __init__ (self, data, default = lambda: ""):
		defaultdict.__init__(self, default, data)

if __name__ == '__main__':
	d = {
		"name": "test"
	}

	t = Test(d)
	print(t["name"])
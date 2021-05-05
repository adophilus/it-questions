d = {
	"name": "test"
}

def retF ():
	return False

d.__bool__ = retF

if (d):
	print("True")
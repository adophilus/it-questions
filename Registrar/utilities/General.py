# import win32gui
# import win32con
import json
import time
import sys
import requests
import urllib
import base64
from threading import Thread
from re import search, sub, I, escape
from cryptography.fernet import Fernet

fernetDefaultKey = 'bmzUYT20jqyQg8379p-ECPAtRKCCXmNf3QR-lMjjcYA='.encode("UTF-8")

def jsonize (string):
	jsonData = json.loads(string)
	return jsonData

def unjsonize (json_data):
	string = json.dumps(json_data, indent = 4)
	return string

def loadJson (path):
	with open(path, "r") as file:
		data = json.load(file)

		return data

def saveJson (path, data):
	with open(path, "w") as file:
		json.dump(data, file, indent = 4)

def getArgv (self, argName):
	try:
		argIndex = sys.argv.index(argName)
		argValue = sys.argv[argIndex + 1]
		return argValue
	except ValueError:
		return None

def putContentIn (filePath, data):
	with open(filePath, "w") as file:
		file.write(data)

def getContentOf (filePath):
	with open(filePath, "r") as file:
		return file.read()

def getContentOfBinary (filePath):
	with open(filePath, "rb") as file:
		return file.read()

def setImmediate (method, args = {}):

	def _method (method, arguments):
		operation = method(**arguments)

	immediateObj = Thread(target = _method, args = (method, args))
	immediateObj.start()
	return immediateObj

def setTimeout (method, secs = 5, args = {}):

	def _method (method, arguments, secs):
		time.sleep(secs)
		operation = method(**arguments)

	timeoutObj = Thread(target = _method, args = (method, args, secs))
	timeoutObj.start()
	return timeoutObj

def setInterval (method, secs = 10, args = {}):
	def _method (method, arguments, secs):
		while True:
			time.sleep(secs)
			operation = method(**arguments)

			if operation == "end" or operation == "break":
				break

	intervalObj = Thread(target = _method, args = (method, args, secs))
	intervalObj.start()
	return intervalObj

def clearTimeout (timeoutObject):
	pass

def clearInterval (intervalObject):
	pass

def httpPost (url, postData = {}, retval = "text"):
	req = requests.post(url, postData)

	if retval == "bytes":
		return req.content
	elif retval == "str" or retval == "string" or retval == "text":
		return req.text
	else:
		return req

def httpGet (url, getData = {}, retval = "text"):
	req = requests.get(url, getData)

	if retval == "bytes":
		return req.content
	elif retval == "str" or retval == "string" or retval == "text":
		return req.text
	else:
		return req

def exp (num1, num2):
	return num1 ** num2

def swapQuotes (txt):
	matchObj = search(r"'", txt, I)
	if matchObj:
		ntxt = sub(r"'", '"', txt)
		return ntxt
	else:
		return txt

def downloadFile (url, filename):
	return urllib.urlretrieve(url, filename)

def searchString (string, regex, ignoreCase = False):
	if ignoreCase:
		match = search(r"%s" % regex, string, I)
	else:
		match = search(r"%s" % regex, string)

	return match

def wait (secs):
	time.sleep(secs)

def hideWindow ():
	program = win32gui.GetForegroundWindow()
	win32gui.ShowWindow(program, win32con.SW_HIDE)

def showWindow ():
	program = win32gui.GetForegroundWindow()
	win32gui.ShowWindow(program, win32con.SW_SHOW)

def fernetGenerateKey ():
	return Fernet.generate_key()

def fernetDecrypt (data, key = None):
	if (key == None):
		key = fernetDefaultKey
	if (not type(data) is type(str("").encode("UTF-8"))):
		data = str(data).encode("utf8")
	return Fernet(key).decrypt(data)

def fernetEncrypt (data, key = None, encoding = "UTF-8"):
	if (key == None):
		key = fernetDefaultKey
	return Fernet(key).encrypt(str(data).encode(encoding))

def fernetDecryptFile (file, key = None):
	if (key == None):
		key = fernetDefaultKey
	with open(file, "rb") as fileO:
		data = fileO.read()
	with open(file, "wb") as fileI:
		fileI.write(fernetDecrypt(data, key))

def fernetEncryptFile (file, key = None):
	if (key == None):
		key = fernetDefaultKey
	with open(file, "rb") as fileO:
		data = fileO.read()
	with open(file, "wb") as fileI:
		fileI.write(fernetEncrypt(data, key))

def fernetOpen (file, key = None):
	if (key == None):
		key = fernetDefaultKey
	with open(file, "rb") as fileO:
		return fernetDecrypt(fileO.read(), key)

def fernetSave (file, data, key = None, encoding = "UTF-8"):
	if (key == None):
		key = fernetDefaultKey
	with open(file, "wb") as fileI:
		fileI.write(fernetEncrypt(data, key, encoding))

def base64Encode (data, encoding = "UTF-8"):
	data = str(data).encode(encoding)
	data = base64.b64encode(data)
	return data

def base64Decode (data):
	data = base64.b64decode(data)
	return data

def sendFalse (message):
	return unjsonize({"error": message, "data": message, "status": False})

def sendTrue (message):
	return unjsonize({"data": message, "status": True})
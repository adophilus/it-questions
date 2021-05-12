from cryptography.fernet import Fernet

from re import search, sub, I, escape
from threading import Thread

from . import config

import json
import time
import sys
import requests
import urllib
import base64

fernetDefaultKey = 'bmzUYT20jqyQg8379p-ECPAtRKCCXmNf3QR-lMjjcYA='.encode("UTF-8")

class FalseDict (dict):
	def __bool__ (self):
		return False

def unjsonize (json_data, *args, **kwargs):
	dict_object = json.loads(json_data, *args, **kwargs)
	return dict_object

def jsonize (dict_object, *args, **kwargs):
	json_data = json.dumps(dict_object, *args, **kwargs)
	return json_data

def loadJson (path, *args, **kwargs):
	with open(path, "r") as file:
		return unjsonize(file.read(), *args, **kwargs)

def saveJson (path, data, *args, **kwargs):
	with open(path, "w") as file:
		file.write(jsonize(data, *args, **kwargs))

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

def sendTrue (data):
	return jsonize({"data": data, "status": True})

def sendFalse (data):
	return jsonize(FalseDict({"error": data, "status": False}))
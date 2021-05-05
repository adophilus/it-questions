def createUserAccount (first_name, last_name, other_names, birthday, email, phone_number, username, password, account_type, classroom = "", department = "", subjects_offered = [], extracurricular_activities = [], subjects_teaching = [], ward_id = ""): # ward_first_name = "", ward_last_name = "", ward_other_names = "", ward_classroom = ""):
	first_name = first_name.strip()
	last_name = last_name.strip()
	other_names = other_names.strip()
	birthday = birthday.strip()
	email = email.strip()
	phone_number = phone_number.strip()
	classroom = classroom.strip()
	department = department.strip()
	ward_id = ward_id.strip()
	# ward_first_name = ward_first_name.strip()
	# ward_last_name = ward_last_name.strip()
	# ward_other_names = ward_other_names.strip()
	# ward_classroom = ward_classroom.strip()

	if (not account_type in globals.config["account"]["types"]):
		return globals.General.unjsonize({"data": config.getMessage("INVALID_ACCOUNT_TYPE"), "status": False})

	if (not globals.methods.Validate.username(username)):
		return globals.General.sendFalse(config.getMessage("INVALID_USERNAME"))

	if (not globals.methods.Validate.password(password)):
		return globals.General.sendFalse(config.getMessage("INVALID_PASSWORD"))

	if (not globals.methods.Validate.email(email)):
		return globals.General.sendFalse(config.getMessage("INVALID_EMAIL"))


	if (len(first_name) == 0 or len(last_name) == 0):
		return globals.General.sendFalse(config.getMessage("INVALID_NAME"))

	# Generate a unique ID for the user
	id = generateUserId(unique = True)
	account_path = os.path.join("data", f"{account_type}s", id)

	# Hash the user's password
	password = globals.methods.encryptPassword(password)

	# Format the user's birthday and set age
	try:
		birthday = datetime.strptime(birthday, "%d/%m/%Y").strftime("%Y-%m-%d")
		birthday = datetime.strptime(birthday, "%Y-%m-%d")
		age = calculateUserAge(birthday)
	except Exception:
		return globals.General.sendFalse(config.getMessage("INVALID_BIRTHDAY"))

	account_details = account_settings = {}


	userAccount = globals.methods.addNewUserToDB(username, password, account_details)
	if (not userAccount):
		return globals.General.sendFalse(config.getMessage("ERROR_OCCURRED"))

	createUserAccountPublicRemarksFile(account_path)

	createUserAccountDetailsFile(account_details, account_path)
	createUserAccountSettingsFile(account_settings, account_path)
	createUserAccountNotificationsFile(account_path)

# def removeUserAccountPublicRemarksFile (id, account_path):
# 	if (os.path.isfile("public_remarks.csv")):
# 		os.unlink(os.path.join(account_path, "public_remarks.csv"))
# 		print(f"[{id}] Removing \"public_remarks.csv\" file...")
# 	else:
# 		print(f"[{id}] File \"public_remarks.csv\" has already been deleted.")

# def removeUserAccountDetailsFile (id, account_path):
# 	rmpath = os.path.join(account_path, "details.json")
# 	if (os.path.isfile(rmpath)):
# 		os.unlink(rmpath)
# 		print(f"[{id}] Removing \"details.json\" file...")
# 	else:
# 		print(f"[{id}] File \"details.json\" has already been deleted.")

# def removeUserAccountSettingsFile (id, account_path):
# 	rmpath = os.path.join(account_path, "settings.json")
# 	if (os.path.isfile(rmpath)):
# 		os.unlink(rmpath)
# 		print(f"[{id}] Removing \"settings.json\" file...")
# 	else:
# 		print(f"[{id}] File \"settings.json\" has already been deleted.")

# def removeUserAccountNotificationsFile (id, account_path):
# 	rmpath = os.path.join(account_path, "notifications.csv")
# 	if (os.path.isfile(rmpath)):
# 		os.unlink(rmpath)
# 		print(f"[{id}] Removing \"notifications.csv\" file...")
# 	else:
# 		print(f"[{id}] File \"notifications.csv\" has already been deleted.")

# def createUserAccountDirectory (account_path):
# 	os.mkdir(account_path)

# def createUserAccountDetailsFile (account_details, account_path):
# 	details = {**account_details}
# 	details["birthday"] = details["birthday"].strftime("%Y-%m-%d")
# 	globals.General.putContentIn(
# 		os.path.join(
# 			account_path,
# 			"details.json"
# 		),
# 		globals.General.unjsonize(
# 			details
# 		)
# 	)

# def createUserAccountNotificationsFile (account_path):
# 	globals.General.putContentIn(os.path.join(account_path, "notifications.csv"), "")

# def createUserAccountPublicRemarksFile (account_path):
# 	globals.General.putContentIn(os.path.join(account_path, "public_remarks.csv"), "")
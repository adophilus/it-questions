from flask import globals

def getGuardianWardStatus (status):
	return globals.config["guardian_ward"]["statuses"].get(status)

def addWardToGuardian (ward, guardian, account_details = None, status = None, fromAddGuardianToWard = False):
	if (not status):
		status = getGuardianWardStatus("AWAITING_CLEARANCE")

	if (not account_details):
		save_account_details = account_details
		account_details = globals.methods.getAccountDetails(guardian.id)
	if (not account_details):
		return False

	ward_profile = {
		ward.id: {
			"status": status
		}
	}

	if (ward.id in account_details["ward"].keys()):
		if (account_details["ward"][ward.id]["status"] == status):
			return False
		account_details["ward"].update(ward_profile)
		if (save_account_details):
			globals.methods.putAccountDetails(guardian.id, account_details, guardian)
		if (not fromAddGuardianToWard):
			return addGuardianToWard(guardian, ward, status, True)
		return account_details

def addGuardianToWard (guardian, ward, status = None, fromAddWardToGuardian = False):
	if (not status):
		status = getGuardianWardStatus("AWAITING_CLEARANCE")

	account_details = globals.methods.getAccountDetails(guardian.id)
	if (not account_details):
		return False

	guardian_profile = {
		guardian.id: {
			"status": status
		}
	}

	if (guardian.id in account_details["guardian"].keys()):
		if (account_details["guardian"][guardian.id]["status"] == status):
			return False
		account_details["guardian"].update(guardian_profile)
		globals.methods.putAccountDetails(ward.id, account_details, ward)
		if (not fromAddWardToGuardian):
			return addWardToGuardian(ward, guardian, None, status, True)
		return True

def removeWardFromGuardian (ward, guardian, fromRemoveGuardianFromWard = False):
	account_details = globals.methods.getAccountDetails(guardian.id)
	if (not account_details):
		return False

	if (ward.id in account_details["ward"].keys()):
		del account_details["ward"][ward.id]
		globals.methods.putAccountDetails(guardian.id, account_details, guardian)
		if (not fromAddGuardianToWard):
			return removeGuardianFromWard(guardian, ward, True)
		return True

def removeGuardianFromWard (guardian, ward, fromRemoveWardFromGuardian = False):
	account_details = globals.methods.getAccountDetails(ward.id)
	if (not account_details):
		return False

	if (guardian.id in account_details["guardian"].keys()):
		del account_details["guardian"][guardian.id]
		globals.methods.putAccountDetails(ward.id, account_details, ward)
		if (not fromRemoveWardFromGuardian):
			return removeWardFromGuardian(ward, guardian, True)
		return True
from flask import globals

def getWards ():
    return

def addWard (wardId, parentId):
    ward = globals.methods.getAccountById(wardId)
    if ((not ward) or ward.ACCOUNT_TYPE != globals.config["account"]["types"]["student"]["name"]):
        errmsg = globals.config.getMessage("INVALID_WARD")
        return globals.General.unjsonize({"error": errmsg, "data": errmsg, "status": False})

    account_details = globals.getAccountDetails(parentId)
    if (not account_details):
        errmsg = globals.config.getMessage("ACCOUNT_DETAILS_RETRIEVAL_FAILED")
        return globals.General.unjsonize({"error": errmsg, "data": errmsg, "status": False})

    for ward in account_details["wards"]:
        if (ward["id"] == wardId):
            errmsg = globals.config.getMessage("WARD_ALREADY_UNDER_PARENT")
            return globals.General.unjsonize({"error": errmsg, "data": errmsg, "status": False})

    account_details["wards"].append({"id": wardId, "name": f"{ward.FIRST_NAME} {ward.LAST_NAME} {ward.OTHER_NAMES}"})
    if (not globals.methods.putAccountDetails(parentId, account_details)):
        errmsg = globals.config.getMessage("ACCOUNT_DETAILS_STORAGE_FAILED")
        return globals.General.unjsonize({"error": errmsg, "data": errmsg, "status": False})

    return globals.General.unjsonize({"data": globals.config.getMessage("WARD_ADD_SUCCESSFUL"), "status": True})

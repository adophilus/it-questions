// this function is highly inefficient because the .csv files will be read each time it is called
exports.lookupID = function (id)
{
	// The code to lookup an ID will go in here
	var check = students.select({"where": {
		"ID": id
	}});

	if (check) {
		return check;
	}
}

exports.checkUsername = function (username)
{
	if (username.length <= 3) {
		// return {
		// 	"msg": "The username is too short!",
		// 	"status": false
		// }
		return false;
	}
	
	if (String(username).match(/\s/)) {
		// return {
		// 	"msg": "The username must not contain any whitespace!",
		// 	"status": false
		// }
		return false;
	}
}

exports.usernameExists = function (username){
	// This checks if the username is already in use
	if (administrators.indexOf(username) > -1 || parents.indexOf(username) > -1 || teachers.indexOf(username) > -1 || students.indexOf(username > -1)) {
		return true;
	}
}

exports.checkPassword = function (password)
{
	if (password.length <= 5) {
		// return {
		// 	"msg": "The password is too short!",
		// 	"status": false
		// }
		return false;
	}

	if (!String(password).match(/\d/)) {
		// return {
		// 	"msg": "The password is not complex!",
		// 	"status": false
		// }
		return false;
	}
}

exports.createAdministratorAccount = function (details)
{
	if (!exports.checkUsername(details.USERNAME) || !exports.checkPassword(details.PASSWORD)) {
		return false;
	}
	
	if (exports.usernameExists(details.USERNAME)) {
		// The username is already in use
		return false;
	}

	do {
		var id = generator.generateKey(ADMIN_ID_LEVEL, "");

		if (!exports.lookupID(id)) break;
	} while (true);

	details["ID"] = id;

	if (!fs.mkdirSync(path.join("data", "administrators", id))) {
		// The user's working folder failed to create
		return false;
	}

	var userDetails = new Array();

	for (detail in details) {

		if (details[detail] == "") {
			// If any of the fields is empty, then return false
			return false;
		}

		userDetails[detail] = details[detail];
	}

	if (!fs.writeFileSync (path.join("data", "administrator", details.ID, "details.json"), JSON.stringify(userDetails))) {
		// The user's details file failed to create
		return false;
	}

	var userSettings = new Array();

	if (!fs.writeFileSync (path.join("data", "administrator", details.ID, "settings.json"), JSON.stringify(userSettings))) {
		// The user's details file failed to create
		return false;
	}

	// create the <teacher_ID>/remarks-made.csv file
	csvdata.write(path.join("data", "administrators", details.ID, "remarks-made.csv"), [], {
		"header": "REMARKEE,DATETIME,REMARK"
	});

	administrators.insert(details);
}

exports.createParentAccount = function (details)
{
	if (!exports.checkUsername(details.USERNAME) || !exports.checkPassword(details.PASSWORD)) {
		return false;
	}
	
	if (exports.usernameExists(details.USERNAME)) {
		// The username is already in use
		return false;
	}

	do {
		var id = generator.generateKey(PARENT_ID_LEVEL, "");

		if (!exports.lookupID(id)) break;
	} while (true);

	details["ID"] = id;

	if (!fs.mkdirSync(path.join("data", "parents", id))) {
		// The user's working folder failed to create
		return false;
	}

	var userDetails = new Array();

	for (detail in details) {

		if (details[detail] == "") {
			// If any of the fields is empty, then return false
			return false;
		}

		userDetails[detail] = details[detail];
	}

	if (!fs.writeFileSync (path.join("data", "parents", details.ID, "details.json"), JSON.stringify(userDetails))) {
		// The user's details file failed to create
		return false;
	}

	var userSettings = new Array();

	if (!fs.writeFileSync (path.join("data", "parents", details.ID, "settings.json"), JSON.stringify(userSettings))) {
		// The user's details file failed to create
		return false;
	}

	parent.insert(details);
}

export.createTeacherAccount = function (details)
{
	if (!exports.checkUsername(details.USERNAME) || !exports.checkPassword(details.PASSWORD)) {
		return false;
	}
	
	if (exports.usernameExists(details.USERNAME)) {
		// The username is already in use
		return false;
	}

	do {
		var id = generator.generateKey(TEACHER_ID_LEVEL, "");

		if (!exports.lookupID(id)) break;
	} while (true);

	details["ID"] = id;

	if (!fs.mkdirSync(path.join("data", "teachers", id))) {
		// The user's working folder failed to create
		return false;
	}

	var userDetails = new Array();

	for (detail in details) {

		if (details[detail] == "") {
			// If any of the fields is empty, then return false
			return false;
		}

		userDetails[detail] = details[detail];
	}

	if (!fs.writeFileSync (path.join("data", "teachers", details.ID, "details.json"), JSON.stringify(userDetails))) {
		// The user's details file failed to create
		return false;
	}

	var userSettings = new Array();

	if (!fs.writeFileSync (path.join("data", "teachers", details.ID, "settings.json"), JSON.stringify(userSettings))) {
		// The user's details file failed to create
		return false;
	}

	// create the <teacher_ID>/remarks-made.csv file
	csvdata.write(path.join("data", "teachers", details.ID, "remarks-made.csv"), [], {
		"header": "REMARKEE,DATETIME,REMARK"
	});
	
	teachers.insert(details);
}

export.createStudentAccount function (details)
{
	if (!exports.checkUsername(details.USERNAME) || !exports.checkPassword(details.PASSWORD)) {
		return false;
	}
	
	if (exports.usernameExists(details.USERNAME)) {
		// The username is already in use
		return false;
	}

	do {
		var id = generator.generateKey(STUDENT_ID_LEVEL, "");

		if (!exports.lookupID(id)) break;
	} while (true);

	details["ID"] = id;

	if (!fs.mkdirSync(path.join("data", "students", id))) {
		// The user's working folder failed to create
		return false;
	}

	var userDetails = new Array();

	for (detail in details) {

		if (details[detail] == "") {
			// If any of the fields is empty, then return false
			return false;
		}

		userDetails[detail] = details[detail];
	}

	// create the <student_ID>/details.json file
	if (!fs.writeFileSync (path.join("data", "students", details.ID, "details.json"), JSON.stringify(userDetails))) {
		// The user's details file failed to create
		return false;
	}

	userStatuses = {
		"active_tests": new Array()
	}
	
	if (!fs.writeFileSync (path.join("data", "students", details.ID, "status.json"), JSON.stringify(userStatuses))) {
		// The user's statuses file failed to create
		return false;
	}

	var userSettings = new Array();

	// create the <student_ID>/settings.json file
	if (!fs.writeFileSync (path.join("data", "students", details.ID, "settings.json"), JSON.stringify(userSettings))) {
		// The user's settings file failed to create
		return false;
	}

	// include an entry in students.csv
	students.insert(details);

	// make the <student_ID>/results folder
	if (!fs.mkdirSync(path.join("data", "students", details.ID, "results"))) {
		return false;
	}

	// make the <student_ID>/subjects-offerred folder
	if (!fs.mkdirSync(path.join("data", "students", details.ID, "subjects-offered"))) {
		return false;
	}

	// make the <student_ID>/private-message folder
	if (!fs.mkdirSync(path.join("data", "students", details.ID, "private-message"))) {
		return false;
	}

	// create the <student_ID>/attendance.csv
	csvdata.write(path.join("data", "students", details.ID, "attendance.csv"), schoolCalendar.csv, {
		"header": "DAY,DAY_TYPE,ACTIVITY,BROADCAST,ATTENDANCE,MARKED_BY"
	});
	
	// create the <student_ID>/public-remarks.csv
	csvdata.write(path.join("data", details.ID, "public-remarks.csv"), [], {
		"header": "ID,COMMENT,DATE,TIME,COMMENT_TYPE"
	});
	
	// create the <student_ID>/public-remarks.csv
	csvdata.write(path.join("data", details.ID, "notifications.csv"), [], {
		"header": "ID,NOTIFICATION,DATE,TIME,NOTIFICATION_TYPE,STATUS"
	});
}
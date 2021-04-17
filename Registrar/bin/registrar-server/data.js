exports.load = function () {

    // load the encryption keys from the installation details file
    fs.readFile(path.normalize("./data/Registrar/installation-details.json"), function (err, data) {
        if (err) {
            console.log("Failed to load the installation details file!");
            process.exit()
        }
        
        var installationDetails = JSON.parse(data);

        global.encryptionKeys = new Array(
            "computer-hostname" + installationDetails["INSTALLATION_DATE"] + installationDetails["INSTALLATION_TIME"],
            installationDetails["INSTALLATION_DATE"] + "computer-hostname" + installationDetails["INSTALLATION_TIME"]
        );

        global.decryptionKeys = new Array(
            installationDetails["INSTALLATION_DATE"] + "computer-hostname" + installationDetails["INSTALLATION_TIME"],
            "computer-hostname" + installationDetails["INSTALLATION_DATE"] + installationDetails["INSTALLATION_TIME"]
        );
    });
    
    // load the app's configuration
    fs.readFile(path.normalize("./data/Registrar/configuration.json"), function (err, data) {
        if (err) {
            console.log("Failed to load the configurations file!");
            process.exit()
        }
        
        global.configuration = JSON.parse(data);
    });

    // load the school's preferences
    fs.readFile(path.normalize("./data/Registrar/school-preferences.json"), function (err, data) {
        if (err) {
            console.log("Failed to load the school preferences file!");
            process.exit()
        }
        
        global.schoolPreferences = JSON.parse(data);
    });

    // load the data records of all user types
    global.administrators = csv.open(path.normalize("./data/administrators/administrators.csv"), function (data) {
        //
    });

    global.parents = csv.open(path.normalize("./data/parents/parents.csv"), function (data) {
        //
    });

    global.teachers = csv.open(path.normalize("./data/teachers/teachers.csv"), function (data) {
        //
    });

    global.students = csv.open(path.normalize("./data/students/students.csv"), function (data) {
        //
    });

    // load miscellaneous data records
    global.questions = csv.open(path.normalize("./data/questions/questions.csv"), function (data) {
        //
    });

    global.schoolSessions = csv.open(path.normalize("./data/school-sessions/school-sessions.csv"), function (data) {
        //
    });

    // load the school calendar
    global.schoolCalendar = csv.open(path.normalize("./data/Registrar/school-calendar.csv"), function (data) {
        //
    });
    
    // load the running processes file
    global.runningProcesses = csv.open(path.normalize("./data/Registrar/running-processes.csv"), function (data) {
        //
    });
}

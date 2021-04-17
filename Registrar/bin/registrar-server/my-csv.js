var csvdata = require("csvdata");
var path = require("path");
var fs = require("fs");

class MyCSV
{
    constructor (filePath, openCallback) {
        this.filePath = filePath;
        this.header = new Array();
        this.fields = new Array();
        return this.open(openCallback);
    }

    parse () {
        for (var row of this.csv) {

            for (var field in row) {

                if (this.header.indexOf(field) == -1) {

                    this.header.push(field);
                    this.fields[field] = new Array();
                }

                this.fields[field].push(row[field]);
            }
        }

        return this;
    }

    selectAll () {
        return this.csv;
    }

    deleteAll () {
        this.csv = new Array();

        for (var field in this.header) {
            this.fields[field] = new Array();
        }

        return this;
    }

    select (options) {
        if (!options) options = {};
        var index = -1;

        if (options.where) {
            for (var field in options.where) {
                if (this.header.indexOf(field) == -1) {
                    return false;
                }
            }

            for (var field in options.where) {
                index = this.fields[field].indexOf(options.where[field]);
            }

            if (index > -1) {
                return this.csv[index];
            }
        }

        return false;
    }

    insert (obj, options) {
        if (!options) options = {};
        var index = -1;

        for (var field in obj) {
            if (this.header.indexOf(field) == -1) {
                return false;
            }
        }

        if (options.where) {
            for (var field in options.where) {
                if (this.header.indexOf(field) == -1) {
                    return false;
                }
            }

            for (var field in options.where) {
                index = this.fields[field].indexOf(options.where[field]);
            }
        }

        for (var field in obj) {
            if (index > -1) {
                this.fields[field].splice(index, 0, obj[field]);
            }
            else {
                this.fields[field].push(obj[field]);
            }
        }

        if (index > -1) {
            this.csv.splice(index, 0, obj);
        }
        else {
            this.csv.push(obj);
        }

        return this;
    }

    update (obj, options) {
        if (!options) options = {};
        var index = -1;

        for (var field in obj) {
            if (this.header.indexOf(field) == -1) {
                return false;
            }
        }

        if (options.where) {
            for (var field in options.where) {
                if (this.header.indexOf(field) == -1) {
                    return false;
                }
            }

            for (var field in options.where) {
                index = this.fields[field].indexOf(options.where[field]);
            }
        }

        for (var field in obj) {
            if (index > -1) {
                this.fields[field].splice(index, 1, obj[field]);
            }
            else if (!options.where) {
                this.fields[field].push(obj[field]);
            }
        }

        if (index > -1) {
            this.csv.splice(index, 1, obj);
        }
        else if (!options.where) {
            this.csv.push(obj);
        }

        return this;
    }

    delete (options) {
        if (!options) options = {};
        var index = -1;

        if (options.where) {
            for (var field in options.where) {
                if (this.header.indexOf(field) == -1) {
                    return false;
                }
            }

            for (var field in options.where) {
                index = this.fields[field].indexOf(options.where[field]);
            }

            // The code to remove a row based on its index
            if (index > -1) {
                for (var field of this.header) {
                    this.fields[field].splice(index, 1);
                }

                this.csv.splice(index, 1);

                return this;
            }
        }

        return false;
    }

    open (callback) {
        var that = this;

        csvdata.load(this.filePath, {"parse": true}).then(function (data, err) {
            that.csv = data;
            callback(data);
        });
    }

    save () {
        return csvdata.write(this.filePath, this.csv, {"header": this.header.join(",")});
    }

    saveAs (filePath) {
        filePath = path.normalize(filePath);

        if (fs.existsSync(path.dirname(filePath))) {
            return csvdata.write(this.filePath, this.csv, {"header": this.header.join(",")});
        }
    }
}

exports.open = function (filePath, callback) {

    filePath = path.normalize(filePath);

    if (fs.existsSync(filePath)) {

        if (fs.statSync(filePath).isFile) {

            return new MyCSV(filePath, callback);
        }
    }
}

global.app = require("express");
global.fs = require("fs");
global.path = require("path");
global.csv = require("./registrar-server/my-csv.js");
global.constants = require("./registrar-server/constants.js");
global.data = require("./registrar-server/data.js");
global.generator = require("./registrar-server/PrivateKeyGenerator.js");

process.chdir("../");

const app = express();
app.set("view engine", "jinja");
app.engine("jinja", require("jinja"));

// nunjucks.configure('views', {
//     autoescape: true,
//     express: app
// });

// app.get('/', function(req, res) {
//     res.render('index.html');
// });

function start ()
{
	data.load();
}

start();
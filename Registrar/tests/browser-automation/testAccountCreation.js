const puppeteer = require("puppeteer");
const fs = require("fs");

function loadJson (file) {
	return JSON.parse(fs.readFileSync(file));
}

function saveJson (file, data) {
	fs.writeFileSync(file, data);
}

function loadConfig () {
	return loadJson("config.json");
}

function saveConfig () {
	return saveJson("config.json", JSON.stringify(config));
}

var config = loadConfig();

async function createAccount (page, account_type = "student") {
	if (config.ids[account_type]) {
		var account = await getAccountById(page, config.ids[account_type]);
		if (account) {
			console.log(`Account already created (${account_type})!`);
			return false;
		}
	}

	await page.goto("http://localhost:4096/signup");

	for (let account_detail_key in config.register[account_type]) {
		await page.type(account_detail_key, config.register[account_type][account_detail_key]);
	}

	await page.click("#form_submit_button");
	sleep(3);
}

async function loginAccount(page, account_type = "student") {
	var is_logged_in = await page.goto("http://localhost:4096/dev/is-logged-in");
	if (await is_logged_in.text() === "true") {
		console.log(`${account_type} is already logged in!`);
		return true;
	}

	await page.goto("http://localhost:4096/signin");
	console.log(`Logging into account ${account_type}...`);

	for (let account_detail_key in config.login[account_type]) {
		await page.type(account_detail_key, config.login[account_type][account_detail_key]);
	}

	await page.click("a.sign-in");
	sleep(3);

	account_id = await getAccountId(page);
	if (account_id) {
		config.ids[account_type] = account_id;
		saveConfig();
	}
}

async function getAccountById (page, id) {
	console.log(`Checking to see if account having an ID of ${id} exists...`);
	var response = await page.goto(`http://localhost:4096/dev/get-account-by-id/${id}`);
	response = await response.json();
	if (response.status) {
		return response.data;
	}
	return false
}

async function getAccountId (page) {
	var response = await page.goto("http://localhost:4096/dev/get-id");
	response = await response.json();
	if (response.status) {
		return response.data;
	}
	return false;
}

async function viewClassroom (page) {
	await page.goto("http://localhost:4096/classroom");
}

function sleep (time) {
	var stopTime = new Date().getTime() + (time * 1000);
	while (new Date().getTime() < stopTime) {}
}

async function startBrowser () {
	return await puppeteer.launch({
		executablePath: "/usr/bin/google-chrome",
		headless: false
	});
}

async function startTest () {
	var browser = await startBrowser();
	var page = await browser.newPage();
	await page.setViewport({
		height: 768,
		width: 1366
	});
	
	if (!await createAccount(page, "student")) {
		await loginAccount(page, "student");
	}

	// config.register.parent["#form_ward_id"] = config.ids.student;
	await viewClassroom(page);
}

startTest();

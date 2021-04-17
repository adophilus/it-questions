function getCookies () {
	var cookies = document.cookie;
	cookies = cookies.split(";");
	
	var returnCookies = new Array();

	for (var cookie of cookies) {
		cookieKeyVal = cookie.split("=");
		var cookieName = cookieKeyVal[0];

		cookieValue = new Array();
		cookieValue["data"] = new Array(cookieKeyVal[1]);
		cookieValue["name"] = cookieName;

		if (cookieValue === undefined || cookieValue["data"] == "") {
			cookieValue["status"] = "most probably deleted";
		}

		cookieValue["data"] = unescape(cookieValue["data"]);
		if (cookieValue["data"] == "" || cookieValue["data"] === undefined) {
			cookieValue["data"] = "{}"
		}
		cookieValue["data"] = JSON.stringify(cookieValue["data"]);
		cookieValue["data"] = JSON.parse(JSON.parse(cookieValue["data"]));
		returnCookies[cookieName] = cookieValue;
	}

	return returnCookies;
}

function setCookie (cookieName, cookieValue, path = "here", expiryDate = "now") {
	var now = new Date();
	if (expiryDate == "now") {
		expiryDate = now.toUTCString();
	}
	else if (expiryDate == "past") {
		now.setMonth(now.getMonth - 1);
		expiryDate = now.toUTCString();
	}
	else if (expiryDate == "future") {
		now.setMonth(now.getMonth + 1);
		expiryDate = now.toUTCString();
	}

	if (path == "here") {
		path = window.location.pathname;
		path = String(path).replace("(^/[\w\d]+/)", "$1");
	}

	cookie = `${cookieName}=${cookieValue}`;
	// cookie += "value=" + cookieValue + ";";
	// cookie += "expires=" + expiryDate + ";";
	// cookie += "path=" + path + ";";
	document.cookie = cookie;
}

function getAccountSearchCookie () {
	var cookie = getCookies()["account_search"];
	if (!(cookie === undefined)) {
		return cookie;
	}
}

function checkAccountSearch () {
	var cookie = getAccountSearchCookie();

	if (!cookie) return false;

	if (cookie["data"]["account_search_code"] == 404) {
		alert(cookie["data"]["message"]);
		setCookie("account_search", "", "here", "past");
	}

	return cookie;
}

function onBodyLoad () {
	checkAccountSearch();
}

onLoad(onBodyLoad);
var $_ = function (element) {
	return document.querySelector(element);
}

var $$_ = function (element) {
	return document.createElement(element);
}

var $___ = new class
{
	constructor (element)
	{
		this.element = document.querySelector(element);
		return this.element;
	}

	click (callback)
	{
		this.element.onclick = function (e)
		{
			callback(e);
		}
	}

	submit (callback)
	{
		this.element.onsubmit = function (e)
		{
			callback(e);
		}
	}

	createElement (element)
	{
		var element = $$.createElement(element);
		this.element.appendChild(element);
		return element;
	}
}

var $$ = document;

var $__ = function (element) {
	return document.querySelectorAll(element);
}

var setCookie = function (cookieArray) {
	for (var set of cookieArray) {

		for (var key in set) {

			cookieVal = key + "=" + set[key] + ";";

			console.log(cookieVal);

			document.cookie = cookieVal;
		}
	}
}


var getCookies = function () {
	return document.cookie;
}
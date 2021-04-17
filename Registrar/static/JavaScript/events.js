var onloadFunctions = new Array();

function onLoad (func) {
	onloadFunctions.push(func);
}

document.querySelector("body").onload = function () {
	for (var func of onloadFunctions) {
		func();
	}
}
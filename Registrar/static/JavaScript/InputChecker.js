class InputChecker
{
	constructor (options) {
		/*
		var options = {
			"element": $_("input"),
			"type": "text",
			"fieldLength": 6,
			"level": 1,
			"callback": callback
		}
		*/

		this.options = {
			"element": document.querySelector("input"),
			"type": "text",
			"fieldLength": 6,
			"level": 1,
			"callback": function () {}
		}

		for (var option in options) {
			this.options[option] = options[option];
		}

		this.element = this.options.element;
	}

	observe () {
		var self = this;

		this.options.element.oninput = function () {
			self.observe_function(self, this);
		}
	}

	observe_function (self, elem) {

		// if (this.respond == false) {
		// 	console.error("Please resolve the error in");
		// 	console.error(this);
		// 	return false;
		// }

		

		if (self.options.type == "text") {

			if (typeof self.options.fieldLength == "object") {

				for (var length of self.options.fieldLength) {

					if (self.options.element.value.length == length) {
						self.options.callback(true);
						return true;
					}
				}

				self.options.callback(false);
				return false;
			}

			if (self.options.element.value.length < self.options.fieldLength) {
				self.options.callback(false);
			}
			else {
				self.options.callback(true);
			}
		}
		else if (self.options.type == "password") {

			// if (self.options.level == 1) {
			if (self.options.element.value.length >= self.options.fieldLength) {
				self.options.callback(true);
			}
			else {
				self.options.callback(false);
			}

			// }
		}
		else if (self.options.type == "email") {

			if (elem.value.match(/@.+\..+$/)) {

				self.options.callback(true);
			}
			else {

				self.options.callback(false);
			}
		}
		else if (self.options.type == "url") {
			if (elem.value.match(/(http|https):\/\/.+?\..+\//)) {

				self.options.callback(true);
			}
			else {

				self.options.callback(false);
			}
		}
	}

	check () {
		var self = this;

		return this.check_function(self, this.options.element);
	}

	check_function (self, elem) {
		// if (self.respond == false) {
		// 	console.error("Please resolve the error in");
		// 	console.error(self);
		// 	return false;
		// }

		if (self.options.type == "text") {

			if (typeof self.options.fieldLength == "object") {
				for (var length of self.options.fieldLength) {

					if (self.options.element.value.length == length) {
						return true;
					}
				}

				return false;
			}

			if (self.options.element.value.length < self.options.fieldLength) {

				return false;
			}
			else {

				return true;
			}
		}
		else if (self.options.type == "password") {

			// if (self.options.level == 1) {

			if (self.options.element.value.length < self.options.fieldLength) {

				return false;
			}
			else {

				return true;
			}
			
			// }
		}
		else if (self.options.type == "email") {

			if (elem.value.match(/@.+\..+$/)) {

				return true;
			}
			else {

				return false;
			}
		}
		else if (self.options.type == "url") {
			if (elem.value.match(/(http|https):\/\/.+?\..+\//)) {

				return true;
			}
			else {

				return false;
			}
		}
	}
}
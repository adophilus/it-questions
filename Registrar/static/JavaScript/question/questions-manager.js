window.is_saving_question = 0;
window.is_loading_question = 0;

class OptionRadioButton {
	constructor (option_number, option_value, option_mark, is_correct_option = false) {
		this.option_number = Number(option_number);
		this.option_value = option_value;
		this.option_marks = option_mark;
		this.option_type = "radio";
		this.is_correct_option = is_correct_option;
		this.is_radio = true;

		this.create();
		this.assignAttributes();
		this.style();
	}

	create () {
		this.containerElement = document.createElement("p");
		this.radioButtonContainer = document.createElement("span");
		this.radioButton = document.createElement("input");
		this.valueElementContainer = document.createElement("span");
		this.valueElement = document.createElement("label");
	}

	assignAttributes () {
		this.containerElement.setAttribute("class", "input-container edit-question-option");

		this.radioButton.checked = this.is_correct_option;
		if (this.is_correct_option) {
			window.correctRadioOption = this;
		}

		this.radioButton.setAttribute("type", "radio");
		this.radioButton.setAttribute("id", "radio" + this.option_number);
		this.radioButton.setAttribute("name", "radio");
		this.radioButton.setAttribute("edit-question-option-number", this.option_number);
		this.radioButton.setAttribute("edit-question-mark", this.marks);
		this.radioButton.setAttribute("class", "sp");

		this.valueElement.setAttribute("type", "text");
		this.valueElement.setAttribute("for", "radio" + this.option_number);
		this.valueElement.setAttribute("class", "option-value");
		this.valueElement.innerHTML = this.option_value;

		this.containerElement.setAttribute("question-option", "");

		var that = this;
		this.radioButton.onclick = function (event) {
			event.preventDefault();
			that.onclick(event, that);
		}
	}

	onclick (event, that) {
		window.optionEntry.val(that.valueElement.innerHTML);
		window.correctOptionSwitch.prop("checked", that.is_correct_option);

		window.selectedOption = that;
		if (that.is_correct_option) {
			window.correctRadioOption = that;
		}
		toggleEditQuestionOptionSettingsBlock(null, "show");
	}

	style () {
		this.radioButtonContainer.style.display = "inline-block";
		this.radioButtonContainer.style.marginRight = "5px";
		this.radioButtonContainer.style.height = "100%";
		this.radioButtonContainer.style.width = "10%";

		this.valueElementContainer.style.display = "inline-block";
		this.valueElementContainer.style.verticalAlign = "middle";
		this.valueElementContainer.style.height = "100%";
		this.valueElementContainer.style.width = "80%";

		this.containerElement.style.padding = "5px";
	}

	element () {
		this.radioButtonContainer.appendChild(this.radioButton);
		this.valueElementContainer.appendChild(this.valueElement);
		this.containerElement.appendChild(this.radioButtonContainer);
		this.containerElement.appendChild(this.valueElementContainer);
		return this.containerElement;
	}

	makeAvailable () {
		window.availableOptions[String(this.option_number)] = this;
	}

	makeScarce () {
		window.availableOptions[String(this.option_number)] = undefined;
	}
}

class OptionTextEntry {
	constructor (option_number, option_value, option_mark, is_correct_option = false, option_match, ignore_case) {
		this.option_number = Number(option_number);
		this.option_value = option_value;
		this.option_marks = option_mark;
		this.option_type = "text";
		this.is_correct_option = is_correct_option;
		this.is_text = true;
		this.match = option_match;
		this.ignore_case = ignore_case;

		this.create();
		this.assignAttributes();
		this.style();
	}

	create () {
		this.containerElement = document.createElement("p");
		this.valueElementContainer = document.createElement("span");
		this.valueElement = document.createElement("input");
	}

	assignAttributes () {
		this.containerElement.setAttribute("class", "input-container edit-question-option");

		// this.valueElement.setAttribute("id", "text" + this.option_number);
		this.valueElement.setAttribute("type", "text");
		this.valueElement.setAttribute("autocomplete", "off");
		this.valueElement.setAttribute("edit-question-option-number", this.option_number);
		this.valueElement.setAttribute("edit-question-mark", this.marks);
		this.valueElement.setAttribute("class", "sp");
		this.valueElement.placeholder = this.option_value;

		this.containerElement.setAttribute("question-option", "");

		var that = this;

		this.valueElement.onkeydown = this.valueElement.onkeyup = this.valueElement.onkeypress = function (event) {
			event.preventDefault();
		}

		this.valueElement.onclick = function (event) {
			that.onclick(event, that);
		}
	}

	onclick (event, that) {
		window.optionEntry.val(that.valueElement.placeholder);
		window.keywordsEntry.val(that.match);
		window.correctOptionSwitch.prop("checked", this.is_correct_option);
		window.caseSensitiveSwitch.prop("checked", !(that.ignore_case));
		window.selectedOption = that;
		toggleEditQuestionOptionSettingsBlock(null, "show");
	}

	style () {
		this.valueElementContainer.style.display = "inline-block";
		this.valueElementContainer.style.verticalAlign = "middle";
		this.valueElementContainer.style.height = "100%";
		this.valueElementContainer.style.width = "80%";

		this.containerElement.style.padding = "5px";
	}

	element () {
		this.valueElementContainer.appendChild(this.valueElement);
		this.containerElement.appendChild(this.valueElementContainer);
		return this.containerElement;
	}

	makeAvailable () {
		window.availableOptions[String(this.option_number)] = this;
	}

	makeScarce () {
		window.availableOptions[String(this.option_number)] = undefined;
	}
}

class OptionCheckBox {
	constructor (option_number, option_value, option_mark, is_correct_option = false) {
		this.option_number = Number(option_number);
		this.option_value = option_value;
		this.option_marks = option_mark;
		this.option_type = "check";
		this.is_correct_option = is_correct_option;
		this.is_check = true;

		this.create();
		this.assignAttributes();
		this.style();
	}

	create () {
		this.containerElement = document.createElement("p");
		this.checkBoxContainer = document.createElement("span");
		this.checkBox = document.createElement("input");
		this.valueElementContainer = document.createElement("span");
		this.valueElement = document.createElement("label");
	}

	assignAttributes () {
		this.containerElement.setAttribute("class", "input-container edit-question-option");

		this.checkBox.checked = this.is_correct_option;

		this.checkBox.setAttribute("type", "checkbox");
		this.checkBox.setAttribute("id", "check" + this.option_number);
		this.checkBox.setAttribute("edit-question-option-number", this.option_number);
		this.checkBox.setAttribute("edit-question-mark", this.marks);
		this.checkBox.setAttribute("class", "sp");

		this.valueElement.setAttribute("for", "check" + this.option_number);
		this.valueElement.setAttribute("class", "option-value");
		this.valueElement.innerHTML = this.option_value;

		this.containerElement.setAttribute("question-option", "");

		var that = this;
		this.checkBox.onclick = function (event) {
			event.preventDefault();
			that.onclick(event, that);
		}
	}

	onclick (event, that) {
		window.optionEntry.val(that.valueElement.innerHTML);
		window.correctOptionSwitch.prop("checked", that.is_correct_option);

		window.selectedOption = that;
		toggleEditQuestionOptionSettingsBlock(null, "show");
	}

	style () {
		this.checkBoxContainer.style.display = "inline-block";
		this.checkBoxContainer.style.marginRight = "5px";
		this.checkBoxContainer.style.height = "100%";
		this.checkBoxContainer.style.width = "10%";

		this.valueElementContainer.style.display = "inline-block";
		this.valueElementContainer.style.verticalAlign = "middle";
		this.valueElementContainer.style.height = "100%";
		this.valueElementContainer.style.width = "80%";

		this.containerElement.style.padding = "5px";
	}

	element () {
		this.checkBoxContainer.appendChild(this.checkBox);
		this.valueElementContainer.appendChild(this.valueElement);
		this.containerElement.appendChild(this.checkBoxContainer);
		this.containerElement.appendChild(this.valueElementContainer);
		return this.containerElement;
	}

	makeAvailable () {
		window.availableOptions[String(this.option_number)] = this;
	}

	makeScarce () {
		window.availableOptions[String(this.option_number)] = undefined;
	}
}

class OptionSwitchBox {
	constructor (option_number, option_value, option_mark, is_correct_option = false, option_match) {
		this.option_number = Number(option_number);
		this.option_value = option_value;
		this.option_marks = option_mark;
		this.option_type = "switch";
		this.is_correct_option = is_correct_option;
		this.is_switch = true;
		this.match = option_match;

		if (option_value == "") {
			this.option_value = "ON|OFF";
		}

		var option_values = this.option_value.split("|");
		this.option_on_value = option_values[0];
		this.option_off_value = option_values[1];

		this.create();
		this.assignAttributes();
	}

	create () {
		var containerElement = document.createElement("p");
		containerElement.setAttribute("class", "input-container edit-question-option");

		this.flipSwitch = new FlipSwitch({
			"on_text": this.option_on_value,
			"off_text": this.option_off_value,
			"container": containerElement,
			"state": "off"
		});

		this.containerElement = this.flipSwitch.flipSwitchOptions.container;
		this.switchBoxLabel = this.flipSwitch.flipSwitchOptions.label;
		this.switchBox = this.flipSwitch.flipSwitchOptions.switch;
		this.valueElement = document.createElement("span");
	}

	assignAttributes () {
		// this.containerElement.setAttribute("class", "input-container edit-question-option");

		// this.switchBox.setAttribute("edit-question-mark", this.marks);
		// this.switchBox.setAttribute("edit-question-option-number", this.option_number);

		// this.switchBoxLabel.setAttribute("class", this.switchBoxLabel.getAttribute("class") + " option-value");

		this.switchBoxLabel.setAttribute("for", "switch" + this.option_number)
		this.switchBox.setAttribute("id", "switch" + this.option_number);
		this.switchBox.checked = false;
		this.valueElement.innerHTML = this.option_value;
		this.containerElement.setAttribute("question-option", "");

		var that = this;
		this.switchBox.onclick = function (event) {
			that.flipSwitch.changeState(that.switchBox.checked);
			that.onclick(event, that);
		}
	}

	onclick (event, that) {
		window.onOptionEntry.val(this.option_on_value);
		window.offOptionEntry.val(this.option_off_value);

		window.switchOptionMatchSelectOn.html(this.option_on_value);
		window.switchOptionMatchSelectOff.html(this.option_off_value);

		window.correctOptionSwitch.prop("checked", that.is_correct_option);

		if (this.option_on_value == this.match) {
			window.switchOptionMatchSelectOff.prop("selected", false);
			window.switchOptionMatchSelectOn.prop("selected", "selected");
		}
		else if (this.option_off_value == this.match) {
			window.switchOptionMatchSelectOn.prop("selected", false);
			window.switchOptionMatchSelectOff.prop("selected", "selected");
		}
		else {
			window.switchOptionMatchSelectOn.prop("selected", false);
			window.switchOptionMatchSelectOff.prop("selected", false);
			window.switchOptionMatchSelectNone.prop("selected", "selected");
		}

		window.selectedOption = that;
		toggleEditQuestionOptionSettingsBlock(null, "show");
	}

	setValue (value_type, value) {
		if (value_type == "on") {
			this.option_on_value = value;
			this.flipSwitch.setOnValue(this.option_on_value);
			window.switchOptionMatchSelectOn.html(this.option_on_value);
		}
		else if (value_type == "off") {
			this.option_off_value = value;
			this.flipSwitch.setOffValue(this.option_off_value);
			window.switchOptionMatchSelectOff.html(this.option_off_value);
		}
		this.option_value = `${this.option_on_value}|${this.option_off_value}`;
		this.valueElement.innerHTML = this.option_value;
	}

	element () {
		return this.flipSwitch.create();
	}

	makeAvailable () {
		window.availableOptions[String(this.option_number)] = this;
	}

	makeScarce () {
		window.availableOptions[String(this.option_number)] = undefined;
	}
}

var options = {
	"radio": OptionRadioButton,
	"text": OptionTextEntry,
	"check": OptionCheckBox,
	"switch": OptionSwitchBox
}

function updateOptionValue (event) {
	var value = event.target.value;

	if (window.selectedOption.is_radio || window.selectedOption.is_check || window.selectedOption.is_switch) {
		window.selectedOption.valueElement.innerHTML = value;
	}
	else if (window.selectedOption.is_text) {
		window.selectedOption.valueElement.placeholder = value;
	}
}

function updateOnOptionValue (event) {
	var value = event.target.value;

	if (window.selectedOption.is_switch) {
		window.selectedOption.setValue("on", value);
	}
}

function updateOffOptionValue (event) {
	var value = event.target.value;

	if (window.selectedOption.is_switch) {
		window.selectedOption.setValue("off", value);
	}
}

function updateOptionKeywords (event) {
	var keywords = event.target.value;

	if (window.selectedOption.is_text) {
		window.selectedOption.match = keywords;
	}
}

function updateOptionMatch (event) {
	var match = event.target.value;
	if (window.selectedOption.is_switch) {
		window.selectedOption.match = match;
	}
}

function updateOptionCorrect (event) {
	var is_correct_option = event.target.checked;

	window.selectedOption.is_correct_option = is_correct_option;
	if (window.selectedOption.is_radio) {
		for (var elem of document.querySelectorAll(".edit-question input[type=radio]")) {
			elem.checked = false;
		}

		if (window.correctRadioOption) {
			window.correctRadioOption.is_correct_option = !(is_correct_option);
		}

		if (is_correct_option) {
			window.correctRadioOption = window.selectedOption;
		}

		window.selectedOption.is_correct_option = is_correct_option;
		window.selectedOption.radioButton.checked = is_correct_option;
	}
	else if (window.selectedOption.is_text) {
		window.selectedOption.is_correct_option = is_correct_option;
	}
	else if (window.selectedOption.is_check) {
		window.selectedOption.is_correct_option = is_correct_option;
		window.selectedOption.checkBox.checked = is_correct_option;
	}
	else if (window.selectedOption.is_switch) {
		window.selectedOption.is_correct_option = is_correct_option;
		// window.selectedOption.flipSwitch.changeState(is_correct_option);
	}
}

function updateOptionCaseSensitive (event) {
	var is_case_sensitive = event.target.checked;
	window.selectedOption.ignore_case = !(is_case_sensitive);
}

function getUserQuestionsList (callback = () => {}) {
	$.ajax({
		url: "/account/questions",
		type: "POST",
		success: function (data) {
			data = JSON.parse(data);
			if (data.status) {
				console.log(data);
				// callback(data.data);
			}
			else {
				alert(data.error);
			}
		},
		error: function (xhr) {
			console.warn(xhr);
		}
	});
}

function displayQuestionsList (questions_list) {
	for (let question_details in questions_list) {
		var questionListContainer = document.createElement("div");
		var questionDetailsContainer = document.createElement("p");
		var questionTitleContainer = document.createElement("span");

		questionDetailsContainer.classList.add("question-list-item");
		questionTitleContainer.innerHTML = question_details.title;

		questionDetailsContainer.appendChild(questionDetailsTitleContainer);
		questionListContainer.appendChild(questionDetailsContainer);
		window.questionsListContainer.append(questionListContainer);
	}
}

function toggleQuestionsList (event, operation = "toggle") {
	var questions_list_container = $(".questions");

	if (operation == "toggle") {
		if (window.displaying["questions_list"]) {
			questions_list_container.fadeOut();
			window.displaying["questions_list"] = false;
		}
		else {
			questions_list_container.fadeIn();
			window.displaying["questions_list"] = true;
		}
	}
	else if (operation == "hide") {
		questions_list_container.fadeOut();
		window.displaying["questions_list"] = false;
	}
	else if (operation == "show") {
		questions_list_container.fadeIn();
		window.displaying["questions_list"] = true;
	}
}

function showQuestionsDetails (event) {
	var container = $(event.target.parentNode);
	var detailsBlock = container.find(".details");
	detailsBlock.slideToggle();
}

function toggleEditQuestionBlock (event, operation = "toggle") {
	var question_edit_container = $(".edit-question");

	if (operation == "toggle") {
		if (window.displaying["question_edit_block"]) {
			question_edit_container.fadeOut();
			window.displaying["question_edit_block"] = false;
		}
		else {
			question_edit_container.fadeIn();
			window.displaying["question_edit_block"] = true;
		}
	}
	else if (operation == "hide") {
		question_edit_container.fadeOut();
		window.displaying["question_edit_block"] = false;
	}
	else if (operation == "show") {
		question_edit_container.fadeIn();
		window.displaying["question_edit_block"] = true;
	}
}

function toggleEditQuestionDetailsBlock (event, operation = "toggle") {
	var question_edit_details_container = $(".edit-question-details");

	if (operation == "toggle") {
		if (window.displaying["question_edit_details_block"]) {
			question_edit_details_container.fadeOut();
			window.displaying["question_edit_details_block"] = false;
		}
		else {
			question_edit_details_container.fadeIn();
			window.displaying["question_edit_details_block"] = true;
		}
	}
	else if (operation == "hide") {
		question_edit_details_container.fadeOut();
		window.displaying["question_edit_details_block"] = false;
	}
	else if (operation == "show") {
		question_edit_details_container.fadeIn();
		window.displaying["question_edit_details_block"] = true;
	}
}

function toggleEditQuestionOptionSettingsBlock (event, operation = "toggle") {
	var option_settings_container = $(".edit-question-option-settings");
	var radio_option_settings = $(".radio-option-settings");
	var text_option_settings = $(".text-option-settings");
	var check_option_settings = $(".check-option-settings");
	var switch_option_settings = $(".switch-option-settings");

	option_settings_container.css("display", "block");
	if (operation == "toggle") {
		if (window.displaying["option_settings_block"]) {
			toggleEditQuestionOptionSettingsBlock(null, "hide");
		}
		else {
			toggleEditQuestionOptionSettingsBlock(null, "show");
		}
	}
	else if (operation == "hide") {
		if (window.displaying["option_settings_block"]) {
			option_settings_container.fadeOut();
		}
		else {
			option_settings_container.css("display", "none");
		}

		radio_option_settings.css("display", "none");
		text_option_settings.css("display", "none");
		check_option_settings.css("display", "none");
		switch_option_settings.css("display", "none");

		window.displaying["option_settings_block"] = false;
	}
	else if (operation == "show") {
		option_settings_container.fadeIn();
		window.displaying["option_settings_block"] = true;

		if (window.selectedOption.is_radio) {
			text_option_settings.css("display", "none");
			check_option_settings.css("display", "none");
			switch_option_settings.css("display", "none");
			radio_option_settings.css("display", "block");
		}
		else if (window.selectedOption.is_text) {
			radio_option_settings.css("display", "none");
			check_option_settings.css("display", "none");
			switch_option_settings.css("display", "none");
			text_option_settings.css("display", "block");
		}
		else if (window.selectedOption.is_check) {
			radio_option_settings.css("display", "none");
			text_option_settings.css("display", "none");
			switch_option_settings.css("display", "none");
			check_option_settings.css("display", "block");
		}
		else if (window.selectedOption.is_switch) {
			radio_option_settings.css("display", "none");
			text_option_settings.css("display", "none");
			check_option_settings.css("display", "none");
			switch_option_settings.css("display", "block");
		}
	}
}

function displayEditQuestionBlock (event) {
	var questionBlock = $(event.target.parentNode.parentNode.parentNode.parentNode);
	var questionId = questionBlock.attr("question-id");
	var questionNumber = 1;
	var totalQuestionNumber = questionBlock.attr("no-of-questions");

	window.constants["currentQuestionBlock"] = questionBlock;
	window.constants["totalQuestionNumber"] = Number(totalQuestionNumber);
	window.constants["questionNumber"] = questionNumber;
	window.constants["questionId"] = questionId;

	// hide the calendar in the right-container
	toggleCalendarDay(null, "hide") || toggleCalendarMonth(null, "hide");

	// hide the profile block and the questions block
	toggleProfile(null, "hide") || toggleQuestionsList(null, "hide");

	// display the edit-question-details-block
	toggleEditQuestionBlock(null, "show") || toggleEditQuestionDetailsBlock(null, "show"); // || toggleEditQuestionOptionSettingsBlock(null, "show");

	loadQuestion(1, questionId, function (questionDetails, data) {
		if (!(questionDetails)) {
			alert("Sorry, an error occurred!");
		}

		data = JSON.parse(data);
		if (!(data.status)) {
			alert(data.error);
		}

		displayQuestionOptions(window.constants["questionNumber"], data.data);
	});
	// displayNextQuestion();
}

function fillQuestionDetailsBlock () {
	var question_id = window.constants["questionId"];

	$.ajax({
		"url": `/handler/question/details/${question_id}`,
		"data": {},
		"type": "GET",
		"success": function (data) {
			data = JSON.parse(data);
			if (data.status) {
				window.currentQuestionDetails = data.data;
				_fillQuestionDetailsBlock();
			}
			else {
				alert(data.error);
				console.warn(data.error);
			}
		},
		"error": function (xhr) {
			console.warn(xhr);
		}
	});
}

function _fillQuestionDetailsBlock () {
	var question_title = document.querySelector("#question_title");
	var number_of_questions = document.querySelector("#number_of_questions");
	var creator_of_question = document.querySelector("#creator_of_question");
	var date_created = document.querySelector("#date_created");
	var last_modified = document.querySelector("#last_modified");
	var total_marks = document.querySelector("#total_marks");

	question_title.innerHTML = window.currentQuestionDetails.title;
	number_of_questions.innerHTML = window.currentQuestionDetails.number_of_questions;
	creator_of_question.innerHTML = window.currentQuestionDetails.creator;
	date_created.innerHTML = window.currentQuestionDetails.date_created;
	last_modified.innerHTML = (window.currentQuestionDetails.last_modified) ? window.currentQuestionDetails.last_modified : window.currentQuestionDetails.date_created;
	total_marks.innerHTML = window.currentQuestionDetails.total_marks;
}

function loadQuestion (question_number, question_id, callback) {
	$.ajax({
		"url": `/handler/question/get/${question_id}/${question_number}`,
		"data": {},
		"type": "GET",
		"success": function (data) {
			window.availableOptions = {};
			callback(true, data);
		},
		"error": function (xhr) {
			callback(false, xhr);
		}
	});
}

function clearQuestionFields () {
	var question_options_holder = $("#question_options_holder");
	window.question_text_holder.val("");
	question_options_holder.html("");
	window.availableOptions = {};
}

function displayQuestionOptions (question_number, question_data) {
	fillQuestionDetailsBlock();
	window.availableOptions = {};
	var question_options_holder = $("#question_options_holder");
	var question_text = question_data.question;

	clearQuestionFields();

	window.question_number_holder.html(String(question_number));
	window.question_text_holder.val(String(question_text));

	var loop_count = 1;

	for (var option in question_data.options) {
		var option_number = option;
		var option_type = question_data.options[option_number].type;
		var option_mark = question_data.options[option_number].mark;
		var option_value = question_data.options[option_number].value;
		var option_match = question_data.options[option_number].match;
		var is_correct_option = false;

		if (option_type == "radio") {
			if (question_data.options.correct.includes(String(loop_count))) {
				is_correct_option = true;
			}
			var option_elem = new options.radio(option_number, option_value, option_mark, is_correct_option);
			option_elem.makeAvailable();
			question_options_holder.append(option_elem.element());
			addQuestionOptionContextMenu(option_elem.element());

		}
		else if (option_type == "text") {
			var ignore_case = question_data.options[option_number].ignore_case;
			if (question_data.options.correct.includes(String(loop_count))) {
				is_correct_option = true;
			}
			var option_elem = new options.text(option_number, option_value, option_mark, is_correct_option, option_match, ignore_case);
			option_elem.makeAvailable();
			question_options_holder.append(option_elem.element());
			addQuestionOptionContextMenu(option_elem.element());
		}
		else if (option_type == "check") {
			if (question_data.options.correct.includes(String(loop_count))) {
				is_correct_option = true;
			}
			var option_elem = new options.check(option_number, option_value, option_mark, is_correct_option);
			option_elem.makeAvailable();
			question_options_holder.append(option_elem.element());
			addQuestionOptionContextMenu(option_elem.element());
		}
		else if (option_type == "switch") {
			if (question_data.options.correct.includes(String(loop_count))) {
				is_correct_option = true;
			}
			var option_elem = new options.switch(option_number, option_value, option_mark, is_correct_option, option_match);
			option_elem.makeAvailable();
			question_options_holder.append(option_elem.element());
			addQuestionOptionContextMenu(option_elem.element());
		}
		// next port of call

		loop_count += 1;
	}
}

function displayQuestionNumber (questionDetails, question_number, data) {
	if (questionDetails === undefined) {
		var question_number = Number($("div[edit-question-number]").val());
		// var question_id = $("div[question-id]").val();

		window.constants["questionNumber"] -= 1;
		var question_id = window.constants["questionId"];

		if (window.constants["questionNumber"] <= 0) {
			window.constants["questionNumber"] = window.constants["totalQuestionNumber"] + window.constants["questionNumber"];
		}

		loadQuestion(window.constants["questionNumber"], question_id, displayPreviousQuestion);

		return true;
	}

	if (!(questionDetails)) {
		alert("Sorry, an error occured!");
		return false;
	}

	data = JSON.parse(data);
	if (!(data.status)) {
		alert(data.error);
		return false;
	}

	displayQuestion(window.constants["questionNumber"], data.data);
}

function updateNumberOfQuestions (number_of_questions) {
	window.constants["currentQuestionBlock"].attr("no-of-questions", number_of_questions);
	window.constants["totalQuestionNumber"] = number_of_questions;
	// window.question_number_holder.html(number_of_questions)
}

function addQuestionNumber () {
	var question_number = window.constants["totalQuestionNumber"] + 1;
	clearQuestionFields();
	updateNumberOfQuestions(question_number);
	window.constants["questionNumber"] = question_number;
	window.question_number_holder.html(question_number);
}

function saveCurrentQuestion (options, callback) {
	if (window.is_saving_question == 1) {
		alert("Please wait until the previous question is done saving...");
		return false;
	}
	else {
		window.is_saving_question += 1;
	}

	var question_id = window.constants["questionId"];
	var question_number = window.constants["questionNumber"];
	var questionData = {
		"question": document.querySelector("textarea[edit-question-text]").value,
		"options": {},
		"correct": new Array()
	}

	var correct_option_available = false;
	for (var option_num in options) {
		if (!options[option_num]) {
			continue;
		}

		var optionData = options[option_num];
		var option = {
			"type": optionData.option_type,
			"mark": optionData.option_marks
		}

		if (optionData.is_correct_option) {
			correct_option_available = true;
			questionData["correct"].push(option_num);
		}

		option["value"] = optionData.valueElement.innerHTML;

		if (optionData.is_text) {
			option["value"] = optionData.valueElement.placeholder;
			option["ignore_case"] = optionData.ignore_case;
			option["match"] = optionData.match;
		}

		if (optionData.is_switch) {
			option["match"] = optionData.match;
		}

		questionData["options"][String(option_num)] = option;
	}

	if (questionData["question"] == "") {
		window.is_saving_question -= 1;
		alert("A question's text cannot be empty!");
		return false;
	}

	if (options.length == 0 || !correct_option_available) {
		window.is_saving_question -= 1;
		alert("A question must have AT LEAST one CORRECT option before it can be saved!");
		return false;
	}

	questionData = JSON.stringify(questionData);

	$.ajax({
		"url": `/handler/question/save/${question_id}/${question_number}`,
		"type": "POST",
		"data": {
			"question_data": questionData
		},
		"success": function (data) {
			data = JSON.parse(data);
			if (data.status) {
				window.availableOptions = {};
				if (callback(data)) {
					alert(data.data);
				}
				window.is_saving_question -= 1;
			}
			else {
				window.availableOptions = {};
				if (callback(data)) {
					alert(data.error);
				}
				window.is_saving_question -= 1;
			}
		},
		"error": function (xhr) {
			console.warn(xhr);
			alert("Server error or inter =net connection error!");
			window.is_saving_question -= 1;
		}
	});
}

function displayPreviousQuestion (questionDetails, data) {
	if (questionDetails === undefined) {
		var question_number = Number($("div[edit-question-number]").val());
		// var question_id = $("div[question-id]").val();

		window.constants["questionNumber"] -= 1;
		var question_id = window.constants["questionId"];

		if (window.constants["questionNumber"] <= 0) {
			window.constants["questionNumber"] = window.constants["totalQuestionNumber"] + window.constants["questionNumber"];
		}

		loadQuestion(window.constants["questionNumber"], question_id, displayPreviousQuestion);

		return true;
	}

	if (!(questionDetails)) {
		alert("Sorry, an error occured!");
		return false;
	}

	try {
		data = JSON.parse(data);
	}
	catch (e) {
		console.warn(e);
		data = {
			"status": data,
			"error": data
		}
	}

	if (!(data.status)) {
		alert(data.error);
		return false;
	}

	displayQuestionOptions(window.constants["questionNumber"], data.data);
}

function displayNextQuestion (questionDetails, data) {
	if (questionDetails === undefined) {
		// var question_id = $("div[question-id]").val();

		window.constants["questionNumber"] += 1;
		var question_id = window.constants["questionId"];

		if (window.constants["questionNumber"] > window.constants["totalQuestionNumber"]) {
			window.constants["questionNumber"] = window.constants["questionNumber"] - window.constants["totalQuestionNumber"];
		}

		loadQuestion(window.constants["questionNumber"], question_id, displayNextQuestion);

		return true;
	}

	if (!(questionDetails)) {
		alert("Sorry, an error occured!");
		return false;
	}

	try {
		data = JSON.parse(data);
	}
	catch (e) {
		console.warn(e);
		data = {
			"status": data,
			"error": data
		}
	}

	if (!(data.status)) {
		alert(data.error);
		return false;
	}


	displayQuestionOptions(window.constants["questionNumber"], data.data);
}


function displayAddQuestionOptionModal () {
	window.addQuestionOptionModal.show();
}

function deleteOption (option_number = 1) {
	var question_options_holder = document.querySelector("#question_options_holder");

	for (var option of document.querySelectorAll("p.edit-question-option")) {
		console.log(option);
		if ($(option).find("input[edit-question-option-number]").attr("edit-question-option-number") == String(option_number)) {
			question_options_holder.removeChild(option);
		}
	}

	window.availableOptions[String(option_number)] = undefined;
}

function addQuestionOptionContextMenu (questionOptionElement) {
	var cmenu = new ContextMenu([
		new ContextMenuItem(
			new ContextMenuItemIcon("entypo-trash"),
			new ContextMenuItemLabel("Delete"),
			new ContextMenuItemCallback(onclickCallback = function (event) {
				console.log("Deleting question option...");

				var context_menu_id = event.target.parentNode.parentNode.getAttribute("context-menu-id");
				var option_number = $(window.customContextMenu[context_menu_id].boundElements[0])
				.find("input[edit-question-option-number]")
				.attr("edit-question-option-number");

				deleteOption(option_number);
			})
		)
	]);

	cmenu.handleContextMenuEvents(questionOptionElement);
	cmenu.create();
}

function addQuestionOption (data) {
	if (!data) {
		return false;
	}

	var option_type = data.toLowerCase();

	var loop_count = 1;
	for (var option_number in window.availableOptions) {
		if (window.availableOptions[option_number]) {
			loop_count++;
		}
	}

	var option_number = String(loop_count);
	var option_value = "";
	var option_mark = 0;
	var ignore_case = true;
	var option_match = "";

	var question_options_holder = $("#question_options_holder");
	var option_elem = new options[option_type](option_number, option_value, option_mark, false, option_match, ignore_case);
	option_elem.makeAvailable();
	question_options_holder.append(option_elem.element());
}

$(document).ready(function () {
	var questionBlocks = $(".question");
	window.optionEntry = $("#option_settings_value_entry");
	window.onOptionEntry = $("#switch_option_settings_on_value_entry");
	window.offOptionEntry = $("#switch_option_settings_off_value_entry");
	window.correctOptionSwitch = $("#option_settings_correct_option");
	window.caseSensitiveSwitch = $("#option_settings_is_case_sensitive");
	window.keywordsEntry = $("#option_settings_keywords");
	window.matchSelect = $("#switch_option_match");
	window.questionsListContainer = $(".question .questions-list");

	window.switchOptionMatchSelectOn = $("#switch_option_on");
	window.switchOptionMatchSelectOff = $("#switch_option_off");
	window.switchOptionMatchSelectNone = $("#switch_option_match_none");

	window.question_text_holder = $("textarea[edit-question-text]");
	window.question_number_holder = $("#question_number");

	window.optionEntry.on("input", updateOptionValue);
	window.offOptionEntry.on("input", updateOffOptionValue);
	window.onOptionEntry.on("input", updateOnOptionValue);
	window.correctOptionSwitch.on("click", updateOptionCorrect);
	window.caseSensitiveSwitch.on("click", updateOptionCaseSensitive);
	window.keywordsEntry.on("input", updateOptionKeywords);
	window.matchSelect.on("change", updateOptionMatch);

	window.addQuestionOptionModal = new ModalBoxSelect({
		"text": "Select the type of option to add",
		"options": ["Radio", "Text", "Check", "Switch"],
		"callback": addQuestionOption
	});

	getUserQuestions(displayUserQuestions);

	for (var questionBlock of questionBlocks) {
		$(questionBlock).click(showQuestionsDetails);

		var editQuestionButton = $(questionBlock).find("#edit_question_button");
		editQuestionButton.click(function (event) {
			displayEditQuestionBlock(event);
			fillQuestionDetailsBlock();
		});
	}

	$(".questions-list #questions_list_toggler").click(toggleQuestionsList);

	// Bind the "previous_question" and the "next_question" buttons to functions
	$(".question-editor #next_question").click(function (e) {
		saveCurrentQuestion(window.availableOptions, function (data) {
			toggleEditQuestionOptionSettingsBlock(null, "hide");
			displayNextQuestion();
			return !(data);
		});
	});

	$(".question-editor #previous_question").click(window.availableOptions, function (e) {
		saveCurrentQuestion(window.availableOptions, function (data) {
			toggleEditQuestionOptionSettingsBlock(null, "hide");
			displayPreviousQuestion();
			return !(data);
		});
	});
});

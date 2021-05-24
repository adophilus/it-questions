function getQuestionsAfter (question_id, callback = () => {}) {
	window.questionLoader.css({"display": "block"});
	$.ajax({
		url: `/questions-pool/list/${question_id}`,
		type: "GET",
		data: {},
		success: function (data) {
			window.questionLoader.css({"display": "none"});
			callback(false, data);
		},
		error: function (xhr) {
			window.questionLoader.css({"display": "none"});
			console.warn(xhr);
			callback(xhr);
		}
	});
}

function displayQuestionsList (error, data) {
	if (!data) {
		return false;
	}
	data = JSON.parse(data);
	// console.log(data);

	if (data.length == 0) {
		return false;
	}

	for (var question of data) {
		var questionContainer = document.createElement("div");
		var questionImage = document.createElement("img");
		var questionTitle = document.createElement("span");

		questionContainer.classList.add("class", "question-item");
		questionContainer.classList.add("block");
		questionImage.classList.add("class", "question-image");
		questionImage.setAttribute("draggable", "false");
		questionTitle.classList.add("class", "question-title");

		questionImage.setAttribute("src", question.image_path);
		questionTitle.innerHTML = question.title;

		questionContainer.onclick = function (event) {
			getQuestionDetails(question.id, displayQuestionModal);
		}

		questionContainer.appendChild(questionImage);
		questionContainer.appendChild(questionTitle);
		window.questionsContainer.append(questionContainer);
	}
}

function getQuestionDetails (question_id, callback = () => {}) {
	$.ajax({
		url: `/handler/question/details/${question_id}`,
		type: "GET",
		data: {},
		success: function (data) {
			data = JSON.parse(data);
			
			callback(!data.status, data.data);
		},
		error: function (xhr) {
			console.warn(xhr);
			callback(true, xhr);
		}
	});
}

function displayQuestionModal (error, data) {
	if (error) {
		return false;
	}

	// console.log(data);
	var questionContainer = document.createElement("div");
	var questionImage = document.createElement("img");
	var questionTitle = document.createElement("span");
	var questionDetails = document.createElement("div");
	var questionFooter = document.createElement("div");

	var downloadBtn = document.createElement("button");
	var pullBtn = document.createElement("button");
	var detailsBtn = document.createElement("button");

	var downloadIcon = document.createElement("span");
	var downloadText = document.createElement("span");
	var pullIcon = document.createElement("span");
	var pullText = document.createElement("span");
	var detailsIcon = document.createElement("span");
	var detailsText = document.createElement("span");

	questionContainer.classList.add("modal-question-container");
	questionImage.setAttribute("src", data.image_path);
	questionImage.classList.add("question-image");
	questionImage.setAttribute("draggable", "false");
	questionTitle.classList.add("question-title");
	questionDetails.classList.add("question-details");
	questionFooter.classList.add("question-footer");

	downloadBtn.classList.add("download-btn");
	downloadIcon.classList.add("entypo-download");
	downloadIcon.style.color = "inherit";
	downloadText.style.color = "inherit";
	downloadText.innerHTML = "Download";

	pullBtn.classList.add("pull-btn");
	pullIcon.classList.add("entypo-link");
	pullIcon.style.color = "inherit";
	pullText.style.color = "inherit";
	pullText.innerHTML = "Pull";

	detailsBtn.classList.add("details-btn");
	detailsIcon.classList.add("entypo-doc-text");
	detailsIcon.style.color = "inherit";
	detailsText.style.color = "inherit";
	detailsText.innerHTML = "Details";

	$(window.modalBox.modalBody).empty();
	questionImage.setAttribute("src", data.image_path);
	questionTitle.innerHTML = data.title;
	questionTitle.style.color = "black";

	downloadBtn.appendChild(downloadIcon);
	downloadBtn.appendChild(downloadText);

	pullBtn.appendChild(pullIcon);
	pullBtn.appendChild(pullText);

	detailsBtn.appendChild(detailsIcon);
	detailsBtn.appendChild(detailsText);

	downloadBtn.onclick = function (event) {
		window.open(`/handler/question/download/${data.id}`);
	}

	detailsBtn.onclick = function (event) {
		if (detailsBtn.classList.toString().search("active") == -1) {
			detailsBtn.classList.add("active");
			$(questionDetails).slideDown();
		}
		else {
			detailsBtn.classList.remove("active");
			$(questionDetails).slideUp();
		}
	}

	for (var elem of generateQuestionDetailsElements(data)) {
		questionDetails.appendChild(elem);
	}

	questionFooter.appendChild(downloadBtn);
	if (window.is_logged_in) {
		questionFooter.appendChild(pullBtn);
	}
	questionFooter.appendChild(detailsBtn);

	questionContainer.appendChild(questionImage);
	questionContainer.appendChild(questionTitle);
	questionContainer.appendChild(questionDetails);
	questionContainer.appendChild(questionFooter);

	window.modalBox.modalBody.appendChild(questionContainer);
	window.modalBox.show();
}

function generateQuestionDetailsElements (question_details) {
	var questionDetailsElementsArray = new Array();

	console.log(question_details);

	var dateCreatedContainer = document.createElement("div");
	var dateCreatedLabel = document.createElement("span");
	var dateCreatedValue = document.createElement("span");

	dateCreatedLabel.innerHTML = "Date created";
	dateCreatedValue.innerHTML = question_details.date_created;

	dateCreatedContainer.appendChild(dateCreatedLabel);
	dateCreatedContainer.appendChild(dateCreatedValue);

	var dateCreatedContainer = document.createElement("div");
	var dateCreatedLabel = document.createElement("span");
	var dateCreatedValue = document.createElement("span");

	dateCreatedLabel.innerHTML = "Date created";
	dateCreatedValue.innerHTML = question_details.date_created;

	dateCreatedContainer.appendChild(dateCreatedLabel);
	dateCreatedContainer.appendChild(dateCreatedValue);

	var numberOfQuestionsContainer = document.createElement("div");
	var numberOfQuestionsLabel = document.createElement("span");
	var numberOfQuestionsValue = document.createElement("span");

	numberOfQuestionsLabel.innerHTML = "Number of questions";
	numberOfQuestionsValue.innerHTML = question_details.number_of_questions;

	numberOfQuestionsContainer.appendChild(numberOfQuestionsLabel);
	numberOfQuestionsContainer.appendChild(numberOfQuestionsValue);

	var totalMarksContainer = document.createElement("div");
	var totalMarksLabel = document.createElement("span");
	var totalMarksValue = document.createElement("span");

	totalMarksLabel.innerHTML = "Total marks";
	totalMarksValue.innerHTML = question_details.total_marks;

	totalMarksContainer.appendChild(totalMarksLabel);
	totalMarksContainer.appendChild(totalMarksValue);

	questionDetailsElementsArray.push(dateCreatedContainer);
	questionDetailsElementsArray.push(numberOfQuestionsContainer);
	questionDetailsElementsArray.push(totalMarksContainer);
	return questionDetailsElementsArray;
}

$(document).ready(function() {
	window.questionsContainer = $(".questions-container");
	window.questionLoader = $(".question-loader");
	window.modalBox = new ModalBox2();
	getQuestionsAfter("none", displayQuestionsList);
});

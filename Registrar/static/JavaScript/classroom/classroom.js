function getClassroomMessages (classroom_id, callback) {
	console.log("getting");
	$.ajax({
		url: `/classroom/${classroom_id}/message`,
		type: "GET",
		data: {},
		success: function (data) {
			data = JSON.parse(data);

			if (data.status) {
				callback(data);
			}
			else {
				console.log(data.error + " " + classroom_id);
			}
		},
		error: function (xhr) {
			console.warn(xhr);
		}
	});
}

function displayClassroomMessages (data, classroom_id, first_call = false) {
	if (first_call) {
		console.log("making 'first_call' with classroom_id: " + classroom_id);
		getClassroomMessages(classroom_id, displayClassroomMessages);
		return;
	}

	console.log("bypassing 'first_call'");
	if (!data.status) {
		return;
	}

	for (let message of data.data) {
		var classroomMessageContainer = document.createElement("div");
		var classroomMessageBody = document.createElement("p");
		var classroomMessageDetails = document.createElement("div");
		var classroomMessageDetailsDateSent = document.createElement("small");

		classroomMessageBody.innerHTML = message.message;
		classroomMessageDetailsDateSent.innerHTML = message.date_sent;

		classroomMessageContainer.classList.add("list");
		classroomMessageBody.classList.add("message");
		classroomMessageDetails.classList.add("message-details");
		classroomMessageDetailsDateSent.classList.add("date-sent");
		classroomMessageDetailsDateSent.classList.add("scnd-font-color");

		classroomMessageDetails.appendChild(classroomMessageDetailsDateSent);
		classroomMessageContainer.appendChild(classroomMessageBody);
		classroomMessageContainer.appendChild(classroomMessageDetails);

		window.activeClassroomMessageContainer.append(classroomMessageContainer);
	}
}

function sendClassroomMessage (classroom_id, message) {
	$.ajax({
		url: `/classroom/${classroom_id}/message`,
		type: "PUT",
		data: {
			message: message
		},
		success: function (data) {
			data = JSON.parse(data);
			if (data.status) {
				console.log(data.data);
				window.window.classroomMessageEntry.val("");
			}
			else {
				alert(data.error);
			}
		}
	});
}

function setActiveClassroom (event) {
	// var elem = $(event.target);
	var classroomsListElement = document.querySelector(".classrooms-list");

	if (classroomsListElement) {
		classroomsListElement.classList.add("classroom");
		classroomsListElement.classList.remove("classrooms-list");
	}

	console.log(event.target.getAttribute("classroom-id"));
	displayClassroomMessages(null, event.target.getAttribute("classroom-id"), true);
	window.activeClassroom = {
		id: event.target.getAttribute("classroom-id"),
		// refresher: setInterval(displayClassroomMessages, 2000, null, event.target.getAttribute("classroom-id"), false)
	}
}

function unsetActiveClassroom (event) {
	clearInterval(window.activeClassroom.refresher);

	getClassroomsList(displayClassroomsList);
	var classroomElement = document.querySelector(".classroom");

	if (classroomElement) {
		classroomElement.classList.add("classrooms-list");
		classroomElement.classList.remove("classroom");
	}
}

function displayClassroomsList (data, err) {
	if (err) {
		console.warn(data)
		return false;
	}

	var classrooms_list = data;

	window.classroomsListContainer.empty();
	if (classrooms_list.length === 0) {
		var containerElement = document.createElement("div");
		var containerTextElement = document.createElement("p");

		containerElement.classList.add("list");
		containerTextElement.classList.add("title");
		containerTextElement.classList.add("scnd-font-color");

		containerTextElement.innerHTML = "No classrooms available!";

		containerElement.appendChild(containerTextElement);
		window.classroomsListContainer.append(containerElement);
		return true;
	}

	for (let classroomDetails of classrooms_list) {
		var classroomListContainerElement = document.createElement("div");
		var classroomListImageElement = document.createElement("img");
		var classroomListTitleElement = document.createElement("p");

		classroomListContainerElement.classList.add("list");
		classroomListImageElement.classList.add("profile");
		classroomListTitleElement.classList.add("title");

		classroomListContainerElement.setAttribute("title", `ID: ${classroomDetails.id}`);
		classroomListContainerElement.setAttribute("classroom-id", classroomDetails.id);
		classroomListImageElement.setAttribute("src", classroomDetails.image);
		classroomListImageElement.setAttribute("draggable", "false");
		classroomListTitleElement.innerHTML = classroomDetails.name;

		classroomListContainerElement.onclick = setActiveClassroom;

		classroomListContainerElement.appendChild(classroomListImageElement);
		classroomListContainerElement.appendChild(classroomListTitleElement);
		window.classroomsListContainer.append(classroomListContainerElement);
	}

	return true;
}

function getClassroomsList (callback) {
	$.ajax({
		url: `/${window.Account.type}/classroom/list`,
		type: "POST",
		data: {},
		success: function (data) {
			data =  JSON.parse(data);
			callback(data.data, null);
		},
		error: function (xhr) {
			callback(null, xhr);
		}
	})
}

$(document).ready(function () {
	window.activeClassroom = new Object();
	window.activeClassroomMessageContainer = $(".active-classroom .messages .list");
	window.classroomsListContainer = $(".classrooms-list .body");
	window.classroomMessageEntry = $("#classroom_message_entry");

	$("#display_classrooms_list_btn").click(function (e) { unsetActiveClassroom(e) });
	$("#message_send_btn").click(function () {
		var message = window.classroomMessageEntry.val().replace(/\s+$/, "");
		if (!message) {
			alert("Empty message!")
			return false;
		}
		else {
			sendClassroomMessage(window.activeClassroom.id, message);
		}
	});

	getClassroomsList(displayClassroomsList);
});
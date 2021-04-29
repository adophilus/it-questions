function getClassroomMessages () {

}

function sendClassroomMessage (classroom_id, message) {
	$.ajax({
		url: `/handler/classroom/${classroom_id}/send-message`,
		type: "POST",
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
	
	window.activeClassroom = {
		"id": event.target.getAttribute("classroom-id")
	}
}

function unsetActiveClassroom (event) {
	getClassroomsList(displayClassroomsList);
	var classroomElement = document.querySelector(".classroom");

	if (classroomElement) {
		classroomElement.classList.add("classrooms-list");
		classroomElement.classList.remove("classroom");
	}
}

function displayClassroomsList (classrooms_list) {
	if (!classrooms_list) {
		return false;
	}

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
		classroomListImageElement.setAttribute("src", classroomDetails.IMAGE_PATH);
		classroomListImageElement.setAttribute("draggable", "false");
		classroomListTitleElement.innerHTML = classroomDetails.NAME;

		classroomListContainerElement.onclick = setActiveClassroom;

		classroomListContainerElement.appendChild(classroomListImageElement);
		classroomListContainerElement.appendChild(classroomListTitleElement);
		window.classroomsListContainer.append(classroomListContainerElement);
	}

	return true;
}

function getClassroomsList (callback) {
	$.ajax({
		url: "/api/classroom/list",
		type: "POST",
		data: {},
		success: function (data) {
			console.log(data);
			data =  JSON.parse(data);
			callback(data.data, null);
		},
		error: function (xhr) {
			callback(xhr);
		}
	})
}

$(document).ready(function () {
	window.activeClassroom = new Object();
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
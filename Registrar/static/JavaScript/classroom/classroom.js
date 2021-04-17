function getClassroomMessages () {
	
}

function setActiveClassroom (event) {
	// var elem = $(event.target);
	var classroomsListElement = document.querySelector(".classrooms-list");
	
	if (classroomsListElement) {
		classroomsListElement.classList.add("classroom");
		classroomsListElement.classList.remove("classrooms-list");
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
	if (classrooms_list.length === 0) {
		window.classroomsListContainer.empty();
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
	window.classroomsListContainer = $(".classrooms-list .body");
	document.querySelector("#display_classrooms_list_btn").onclick = unsetActiveClassroom;
	getClassroomsList(displayClassroomsList);
});
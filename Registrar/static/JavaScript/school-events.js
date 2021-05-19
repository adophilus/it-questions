function toggleSchoolEvents (event, operation = "toggle") {
	var school_events_container = $(".events");

	if (operation == "toggle") {
		if (window.displaying["school_events"]) {
			school_events_container.fadeOut();
			window.displaying["school_events"] = false;
		}
		else {
			school_events_container.fadeIn();
			window.displaying["school_events"] = true;
		}
	}
	else if (operation == "hide") {
		 school_events_container.fadeOut();
		window.displaying["school_events"] = false;
	}
	else if (operation == "show") {
		school_events_container.fadeIn();
		window.displaying["school_events"] = true;
	}
}

function getSchoolEvents (callback) {
	// obsolete?
	if (window.schoolEvents === undefined) {
		window.schoolEvents = new Array();
	}

	$.ajax({
		"url": "/school/event/get",
		"data": {},
		"type": "POST",
		"success": function (data) {
			data = JSON.parse(data);
			if (data.status) {
				callback(data.data);
			}
		},
		"error": function (xhr) {
			console.warn(xhr);
		}
	})
}

function displaySchoolEvents (school_events) {
	for (let school_event of school_events) {
		addSchoolEventToDisplay(school_event);
	}
}

function continuouslyGetSchoolEvents () {
	setInterval(getSchoolEvents, (1000 * 3), displaySchoolEvents);
}

function addSchoolEventToDisplay (schoolEvent) {
	if (window.schoolEvents.indexOf(schoolEvent.id) > -1) {
		return false;
	}

	var listElement = document.createElement("div");
	listElement.setAttribute("class", "list");

	var schoolEventElement = document.createElement("div");
	schoolEventElement.setAttribute("class", "school-event");
	schoolEventElement.setAttribute("school-event-id", schoolEvent.id);

	var schoolEventTitle = document.createElement("p");
	schoolEventTitle.setAttribute("class", "school-event-title");

	var schoolEventDetails = document.createElement("p");
	schoolEventDetails.setAttribute("class", "school-event-details");

	var schoolEventDetailsDate = document.createElement("span");
	schoolEventDetailsDate.setAttribute("class", "school-event-details-date scnd-font-color");
	schoolEventDetailsDate.innerHTML = schoolEvent.datetime;

	$(schoolEventTitle).html(schoolEvent.event);
	schoolEventDetails.appendChild(schoolEventDetailsDate);
	listElement.appendChild(schoolEventTitle);
	listElement.appendChild(schoolEventDetails);
	schoolEventElement.appendChild(listElement);
	document.querySelector(".school-events").appendChild(schoolEventElement);

	window.schoolEvents.push(schoolEvent.id);
}

$(document).ready(function (){
	$("#school_events_toggler").click(toggleSchoolEvents);

	continuouslyGetSchoolEvents();
});
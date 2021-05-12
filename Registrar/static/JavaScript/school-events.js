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

function __getSchoolEvents (callback, after_event_id) {
    // $.ajax({
    //     "url": "/handler/school/events/get/" + after_event_id,
    //     "data": {},
    //     "type": "GET",
    //     "success": function (data) {
    //         data = JSON.parse(data);
    //         callback(data);
    //     },
    //     "error": function (xhr) {
    //         console.warn(xhr);
    //     }
    // });
    console.log("yet to be refactored! " + after_event_id);
}

function getSchoolEvents () {
	if (window.schoolEvents === undefined) {
		window.schoolEvents = new Array();
	}

	__getSchoolEvents(function (events) {
		var schoolEventsNumberElement = document.querySelector("div[number-of-unseen-school-events]");

		if (schoolEventsNumberElement.getAttribute("number-of-unseen-school-events") == "") {
			schoolEventsNumberElement.setAttribute("number-of-unseen-school-events", events.length);
			schoolEventsNumberElement.innerHTML = events.length;
		}
		else {
			if (Number(schoolEventsNumberElement.getAttribute("number-of-unseen-school-events")) == 0) {
				schoolEventsNumberElement.style.display = "none";
				schoolEventsNumberElement.setAttribute("number-of-unseen-school-events", events.length);
			}
		}

	    for (var event of events) {
	    	window.schoolEvents.push(event["ID"]);
	        addSchoolEventToDisplay(event);
	    }

	    if (window.schoolEvents.length == 0) {
			$(".school-event-none").css({"display": "block"});
		}
		else {
			$(".school-event-none").css({"display": "none"});
		}
	}, (window.schoolEvents[window.schoolEvents.length - 1]) ? window.schoolEvents[window.schoolEvents.length - 1] : "null");
}

function continuouslyGetSchoolEvents () {
	setInterval(getSchoolEvents, (1000 * 3));
}

function addSchoolEventToDisplay (schoolEvent) {
    var listElement = document.createElement("div");
    listElement.setAttribute("class", "list");

    var schoolEventElement = document.createElement("div");
    schoolEventElement.setAttribute("class", "school-event");
    schoolEventElement.setAttribute("school-event-id", schoolEvent["ID"]);

    var schoolEventTitle = document.createElement("p");
    schoolEventTitle.setAttribute("class", "school-event-title");

    var schoolEventDetails = document.createElement("p");
    schoolEventDetails.setAttribute("class", "school-event-details");

    var schoolEventDetailsDate = document.createElement("span");
    schoolEventDetailsDate.setAttribute("class", "school-event-details-date scnd-font-color");
    schoolEventDetailsDate.innerHTML = schoolEvent["DATE"];

    $(schoolEventTitle).html(schoolEvent["EVENT"]);
    schoolEventDetails.appendChild(schoolEventDetailsDate);
    listElement.appendChild(schoolEventTitle);
    listElement.appendChild(schoolEventDetails);
    schoolEventElement.appendChild(listElement);
    document.querySelector(".school-events").appendChild(schoolEventElement);
}

$(document).ready(function (){
	$("#school_events_toggler").click(toggleSchoolEvents);

	getSchoolEvents();
    // continuouslyGetSchoolEvents();
});
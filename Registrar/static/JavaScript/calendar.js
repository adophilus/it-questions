function toggleCalendarDay (event, operation = "toggle") {
    var calendar_day_container = $(".calendar-day");

    if (operation == "toggle") {
	    if (window.displaying["calendar_day"]) {
	        calendar_day_container.fadeOut();
	        window.displaying["calendar_day"] = false;
	    }
	    else {
	        calendar_day_container.fadeIn();
	        window.displaying["calendar_day"] = true;
	    }
	}
	else if (operation == "hide") {
        calendar_day_container.fadeOut();
        window.displaying["calendar_day"] = false;
	}
	else if (operation == "show") {
        calendar_day_container.fadeIn();
        window.displaying["calendar_day"] = true;
	}
}

function toggleCalendarMonth (event, operation = "toggle") {
    var calendar_month_container = $(".calendar-month");

    if (operation == "toggle") {
	    if (window.displaying["calendar_month"]) {
	        calendar_month_container.fadeOut();
	        window.displaying["calendar_month"] = false;
	    }
	    else {
	        calendar_month_container.fadeIn();
	        window.displaying["calendar_month"] = true;
	    }
	}
	else if (operation == "hide") {
        calendar_month_container.fadeOut();
        window.displaying["calendar_month"] = false;
	}
	else if (operation == "show") {
        calendar_month_container.fadeIn();
        window.displaying["calendar_month"] = true;
	}
}
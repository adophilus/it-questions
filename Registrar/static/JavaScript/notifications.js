function toggleNotifications (event, operation = "toggle") {
    var notifications_container = $(".notifications");

    if (operation == "toggle") {
        if (window.displaying["notifications"]) {
            notifications_container.fadeOut();
            window.displaying["notifications"] = false;
        }
        else {
            notifications_container.fadeIn();
            window.displaying["notifications"] = true;
        }
    }
    else if (operation == "hide") {
        notifications_container.fadeOut();
        window.displaying["notifications"] = false;
    }
    else if (operation == "show") {
        notifications_container.fadeIn();
        window.displaying["notifications"] = true;
    }
}

$(document).ready(function () {
    $("#notifications_toggler").click(toggleNotifications);
});
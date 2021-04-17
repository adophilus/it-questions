function toggleProfile (event, operation = "toggle") {
    var profile_container = $(".profile");

    if (operation == "toggle") {
        if (window.displaying["user_profile"]) {
            profile_container.fadeOut();
            window.displaying["user_profile"] = false;
        }
        else {
            profile_container.fadeIn();
            window.displaying["user_profile"] = true;
        }
    }
    else if (operation == "hide") {
        profile_container.fadeOut();
        window.displaying["user_profile"] = false;
    }
    else if (operation == "show") {
        profile_container.fadeIn();
        window.displaying["user_profile"] = true;
    }
}

function togglePublicRemarks (event, operation = "toggle") {
    var public_remarks_container = $("#public_remarks");

    if (operation == "toggle") {
        if (window.displaying["public_remarks"]) {
            public_remarks_container.fadeOut();
            $(this).find("span").removeClass("fontawesome-comment");
            $(this).find("span").addClass("fontawesome-comment-alt");
            window.displaying["public_remarks"] = false;
        }
        else {
            public_remarks_container.fadeIn();
            $(this).find("span").removeClass("fontawesome-comment-alt");
            $(this).find("span").addClass("fontawesome-comment");
            window.displaying["public_remarks"] = true;
        }
    }
    else if (operation == "hide") {
        public_remarks_container.fadeOut();
        $(this).find("span").removeClass("fontawesome-comment");
        $(this).find("span").addClass("fontawesome-comment-alt");
        window.displaying["public_remarks"] = false;
    }
    else if (operation == "show") {
        public_remarks_container.fadeIn();
        $(this).find("span").removeClass("fontawesome-comment-alt");
        $(this).find("span").addClass("fontawesome-comment");
        window.displaying["public_remarks"] = true;
    }
}

$(document).ready(function () {
    $("#profile_toggler").click(toggleProfile);

    $("#public_remarks_toggler").click(togglePublicRemarks);

    $(".profile-menu").click(logoutUser);
});
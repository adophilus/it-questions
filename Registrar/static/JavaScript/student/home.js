window.displaying["classroom"] = true;

$("#classroom_toggle").click(function () {
    if (window.displaying["classroom"]) {
        $(".calendar-day").fadeOut();
        $(".calendar-month").fadeOut();
        window.displaying["classroom"] = false;
    }
    else {
        window.displaying["classroom"] = true;
        $(".calendar-day").fadeIn();
        $(".calendar-month").fadeIn();
    }
});

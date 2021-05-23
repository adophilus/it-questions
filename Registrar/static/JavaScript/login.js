function login () {
    var username = $("#sign-in-form #form-email-username").val();
    var password = $("#sign-in-form #form-password").val();
    var remember_me = $("#sign-in-form #form-remember_me").val();
    $.ajax({
        "url": "/handler/login",
        "type": "POST",
        "data": {
            "email_username": username,
            "password": password,
            "remember_me": true
        },
        "success": function (data) {
            data = JSON.parse(String(data));
            console.log(data);
            if (data.status) {
                window.location.replace(data.data);
            }
            else {
                alert(data.error);
            }
        },
        "error": function (xhr) {
            console.warn(xhr);
        }
    });
}

$(document).ready(function () {
    $("#sign-in-form .sign-in").click(login);
});

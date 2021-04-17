function login () {
    var username = $("#sign-in-form #form-username").val();
    var password = $("#sign-in-form #form-password").val();
    var remember_me = $("#sign-in-form #form-remember_me").val();
    $.ajax({
        "url": "/handler/login",
        "type": "POST",
        "data": {
            "username": username,
            "password": password,
            "remember_me": true
        },
        "success": function (data) {
            data = JSON.parse(String(data));
            console.log(data);
            if (data.status) {
                var link = document.createElement("a");
                link.setAttribute("href", `/${data.ACCOUNT_TYPE}`);
                link.click();
            }
            else {
                alert(data.data);
            }
        },
        "error": function (xhr) {
            console.warn(xhr);
        }
    });
}

$(document).ready(
    function () {
        $("#sign-in-form .sign-in").click(login);
    }
);

function logoutUser () {
    $.ajax({
        "url": "/handler/logout",
        "type": "POST",
        "data": {"logout":true},
        "success": function (data) {
            console.log(data);
            data = JSON.parse(data);

            if (data.status) {
                var elem = document.createElement("a");
                elem.setAttribute("href", "/login");
                setTimeout(function () {elem.click()}, 3000);
                alert(data.data);
            }
            else {
                alert(data.status);
            }
        },
        "error": function (xhr, status) {
            console.warn(xhr);
            alert(xhr);
        } 
    });
}
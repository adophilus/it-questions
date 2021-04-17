function toggleAccountSettings (event, operation = "toggle") {
    var account_settings_container = $(".account-settings");

    if (operation == "toggle") {
	    if (window.displaying["account_settings"]) {
	        account_settings_container.fadeOut();
	        window.displaying["account_settings"] = false;
	    }
	    else {
	        account_settings_container.fadeIn();
	        window.displaying["account_settings"] = true;
	    }
	}
	else if (operation == "hide") {
		 account_settings_container.fadeOut();
        window.displaying["account_settings"] = false;
	}
	else if (operation == "show") {
		account_settings_container.fadeIn();
        window.displaying["account_settings"] = true;
	}
}

function changePassword (password = null) {
	$.ajax({
		"url": "/handler/account/change/password",
		"type": "POST",
		"data": {
			"password": password,
			"confirm_password": "password1234" //password
		},
		"success": function (data) {
			console.log(data);
			data = JSON.parse(data);
			alert(data.data);
		},
		"error": function (xhr) {
			console.warn(xhr);
		}
	});
}

function saveChanges () {
	var new_password = $(".account-settings .password").val();
	changePassword(new_password);
}

$(document).ready(function () {
    $("#account_settings_toggler").click(toggleAccountSettings);

    $("#save_account_settings_btn").click(saveChanges);
});
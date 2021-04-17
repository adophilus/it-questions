window.displaying["student_teacher_personal_details_block"] = false;
window.displaying["teacher_school_details_block"] = false;

$(document).ready(function (){
	$("#form_birthday").datepicker({
		dateFormat: "dd/mm/yy"
	});

	$("select#form_account_type").on("change", function (){
		if ($(this).children("option:selected").val() == "student") {
			$("#student_teacher_personal_details_block").css({"display": "block"});
			$("#student_school_details_block").css({"display": "block"});
			$(".student_school_details_block").css({"display": "block"});
			$("#teacher_school_details_block").css({"display": "none"});
			$("#parent_student_details_block").css({"display": "none"});
			$("#parent_titular").css({"display": "none"});
			$("#student_teacher_titular").css({"display": "block"});
		} else if ($(this).children("option:selected").val() == "teacher") {
			$("#student_teacher_personal_details_block").css({"display": "block"});
			$("#teacher_school_details_block").css({"display": "block"});
			$("#student_school_details_block").css({"display": "none"});
			$(".student_school_details_block").css({"display": "none"});
			$("#parent_student_details_block").css({"display": "none"});
			$("#parent_titular").css({"display": "none"});
			$("#student_teacher_titular").css({"display": "block"});
		} else if ($(this).children("option:selected").val() == "parent") {
			$("#parent_student_details_block").css({"display": "block"});
			$("#parent_titular").css({"display": "block"});
			$("#student_teacher_titular").css({"display": "none"});
			$("#student_teacher_personal_details_block").css({"display": "none"});
			$(".student_school_details_block").css({"display": "none"});
			$("#student_school_details_block").css({"display": "block"});
		}
	});

	fetch("/handler/list-of-classrooms").then(response => {
		response.text().then(response => {
			// console.log("Classrooms:");
			// console.log(response);
			$("#form_classroom").autocomplete({
				source: JSON.parse(response),
				"minLength": 0,
			});

			$("#form_ward_classroom").autocomplete({
				source: JSON.parse(response),
				"minLength": 0,
			});
		});
	});

	$("#form_submit_button").click(function (){
		// Open to all
		var first_name = $("#form_first_name").val();
		var last_name = $("#form_last_name").val();
		var other_names = $("#form_other_names").val();
		var birthday = $("#form_birthday").val();
		var email = $("#form_email").val();
		var phone_number = $("#form_phone_number").val();

		// General Credentials
		var username = $("#form_username").val();
		var password = $("#form_password").val();
		var account_type = $("#form_account_type").children("option:selected").val();

		// Students exclusively
		var classroom = $("#form_classroom").val();
		var department = $("#form_department").val();
		var subjects_offered = $("#form_subjects_offered").val();
		var extracurricular_activities = $("#form_extracurricular_activities").val();

		// Teachers exclusively
		var subjects_teaching = $("#form_subjects_teaching").val();

		// Parent's exclusively
		var ward_id = $("#form_ward_id").val();
		// var ward_first_name = $("#form_ward_first_name").val();
		// var ward_last_name = $("#form_ward_last_name").val();
		// var ward_other_names = $("#form_ward_other_names").val();
		// var ward_classroom = $("#form_ward_classroom").val();

		if (first_name == "" || last_name == "") {
			alert("Neither first name  nor last name can be empty");
			return false;
		}
		else if (!(new InputChecker({"element": document.querySelector("#form_email"), "type": "email"}).check())) {
			alert("Invalid email address!");
			return false;
		}
		else if (username == "" || password == "") {
			alert("Invalid username or password!");
			return false;
		}
		// else if(account_type == "parent") {
		// 	if (ward_first_name == "" || ward_last_name == "") {
		// 		alert("Please fill in the name of your ward!");
		// 		return false;
		// 	}
		// 	else if (ward_classroom == "") {
		// 		alert("Please fill in the classroom of your ward!");
		// 		return false;
		// 	}
		// }
		else if(account_type == "teacher") {
			if (subjects_teaching == "")  {
				alert("Please enter the subjects you can teach!");
				return false;
			}
		}
		else if(account_type == "student") {
			if (classroom == "") {
				alert("Please fill in your classroom name!");
				return false;
			}
			else if (subjects_offered == "") {
				alert("Please enter the list of subjects you offer!");
				return false;
			}
		}

		$.ajax({
			"type": "POST",
			"url": "/handler/signup",
			"data": {
				// Eveeryone's fields
				"first_name": first_name,
				"last_name": last_name,
				"other_names": other_names,
				"birthday": birthday,
				"email": email,
				"phone_number": phone_number,
				"username": username,
				"password": password,
				"account_type": account_type,

				// Student's fields
				"classroom": classroom,
				"department": department,
				"subjects_offered": subjects_offered,
				"extracurricular_activities": extracurricular_activities,

				// Teacher fields
				"subjects_teaching": subjects_teaching,

				// Parent fields
				"ward_id": ward_id,
				// "ward_first_name": ward_first_name,
				// "ward_last_name": ward_last_name,
				// "ward_other_names": ward_other_names,
				// "ward_classroom": ward_classroom
			},
			"success": function (data) {
				console.log(data);
				data = JSON.parse(data);
				if (data.status) {
					var link = document.createElement("a");
					link.setAttribute("href", "/login");
					alert(data.data);
					setTimeout((link) => {
						link.click();
					}, 2000, link)
				}
				else {
					alert(data.data);
				}
			},
			"error": function (xhr) {
				console.warn(xhr);
			}
		})
	});
});
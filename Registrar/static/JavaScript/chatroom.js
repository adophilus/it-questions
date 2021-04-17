function toggleChatroom (event, operation = "toggle") {
    var chatroom_container = $(".chatroom");

    if (operation == "toggle") {
	    if (window.displaying["chatroom"]) {
	        chatroom_container.fadeOut();
	        window.displaying["chatroom"] = false;
	    }
	    else {
	        chatroom_container.fadeIn();
	        window.displaying["chatroom"] = true;
	    }
	}
	else if (operation == "hide") {
		 chatroom_container.fadeOut();
        window.displaying["chatroom"] = false;
	}
	else if (operation == "show") {
		chatroom_container.fadeIn();
        window.displaying["chatroom"] = true;
	}
}

function displayChatroomsList () {
    var activeChatroom = $(".active-chatroom");

    activeChatroom.fadeOut({"display": "none"}, 1000);
    setTimeout(function () {
        $(".chatrooms-list").fadeIn();
    }, 500);
}

function displayChatroomDetails () {
    console.log("Displaying chatroom details...");
}

function getMyChatroomsList (callback) {
    $.ajax({
        "url": "/handler/chatroom/get",
        "data": {},
        "type": "GET",
        "success": function (data) {
            data = JSON.parse(data);
            callback(data);
        },
        "error": function (xhr) {
            console.warn(xhr);
        }
    });
}

function addChatroomToDisplay (chatroom_details) {
    var html_list_container = document.querySelector(".chatrooms-list");

    var container = document.createElement("div");
    container.setAttribute("class", "chatroom-list-item");
    container.setAttribute("chatroom-id", chatroom_details["id"]);

    var list_container = document.createElement("div");
    list_container.setAttribute("class", "list");

    var chatroom_list_item_title = document.createElement("p");
    chatroom_list_item_title.setAttribute("class", "title");
    chatroom_list_item_title.innerHTML = chatroom_details["name"];
    list_container.appendChild(chatroom_list_item_title);
    container.appendChild(list_container);
    html_list_container.appendChild(container);
}

function sendChat (chat, chatroom_id, callback) {
    $.ajax({
        "url": "/handler/chatroom/chat/add/" + chatroom_id,
        "type": "POST",
        "data" : {
            "chat_message": chat
        },
        "success": function (data) {
            // console.log(data);
            data = JSON.parse(data);

            if (!(data.status)) {
                console.warn(data.error);
                alert(data.error);
            }

            if (callback(data)) {
                var chat = data.data;
                addChatToDisplay(chat);
            }
        },
        "error": function (xhr) {
            console.warn(xhr);
            alert("Sorry, an error occurred!");
        }
    });
}

function addChatToDisplay (chat) {
    window.chat_messages.push(chat.FLOAT_TIME);

    var listElement = document.createElement("div");
    listElement.setAttribute("class", "list");

    var chatElement = document.createElement("div");
    chatElement.setAttribute("class", "chat");

    var chatMessage = document.createElement("p");
    chatMessage.setAttribute("class", "chat-message");

    var chatDetails = document.createElement("p");
    chatDetails.setAttribute("class", "chat-details");

    var chatDate = document.createElement("span");
    chatDate.setAttribute("class", "chat-message-date scnd-font-color");
    chatDate.innerHTML = chat.DATE + " | ";

    var chatTime = document.createElement("span")
    chatTime.setAttribute("class", "chat-message-time scnd-font-color");
    chatTime.innerHTML = chat.TIME;
    
    var chatSender = document.createElement("span")
    chatSender.setAttribute("class", "chat-message-sender scnd-font-color");
    chatSender.innerHTML = `<a href="/user/${chat.SENDER}">${chat.SENDER}</a>`;

    var chatEntry = $("#chat_entry");

    $(chatMessage).html(chat.MESSAGE);
    chatDetails.appendChild(chatDate);
    chatDetails.appendChild(chatTime);
    chatDetails.appendChild(chatSender);
    chatElement.appendChild(chatMessage);
    chatElement.appendChild(chatDetails);
    listElement.appendChild(chatElement);
    var chatsDiv = document.querySelector(".active-chatroom .chats")
    chatsDiv.appendChild(listElement);

    chatEntry.val("");
    chatsDiv = $(chatsDiv);
    chatsDiv.scrollTop(chatsDiv[0].scrollHeight);
}

function loadChats (chatroom_id, callback, message_float_time) {
    // console.log("Message Float Time: " + message_float_time);
    $.ajax({
        "url": `/handler/chatroom/chat/get/${chatroom_id}/${message_float_time}`,
        "type": "GET",
        "data": {},
        "success": function (data) {
            // console.log(data);
            data = JSON.parse(data);
            if (!(data.status)) {
                console.warn(data.error);
                alert(data.error);
            }

            if (callback(data)) {
                // console.log(data.data);
                for (var chat of data.data) {
                    addChatToDisplay(chat);
                }
            }
        }
    });
}

function sendChat (chat, chatroom_id, callback) {
    $.ajax({
        "url": "/handler/chatroom/chat/add/" + chatroom_id,
        "type": "POST",
        "data" : {
            "operation": "post",
            "chat_message": chat
        },
        "success": function (data) {
            // console.log(data);
            data = JSON.parse(data);

            if (!(data.status)) {
                console.warn(data.error);
                alert(data.error);
            }

            if (callback(data)) {
                var chat = data.data;
                addChatToDisplay(chat);
            }
        },
        "error": function (xhr) {
            console.warn(xhr);
            alert("Sorry, an error occurred!");
        }
    });
}

function changeActiveChatroom (chatroom_id) {
    // console.log(event);
    var activeChatroom = $(".active-chatroom");

    $(".chatrooms-list").css({"display": "none"});
    activeChatroom.css({"display": "block"});
    activeChatroom.attr("chatroom-id", chatroom_id);
}

function fillChatroomSpace (chatroom_id) {
    var last_message_float_time = (window.chat_messages[window.chat_messages.length - 1]) ? window.chat_messages[window.chat_messages.length - 1] : null;
    loadChats(chatroom_id, function (chats) {
        return true;
    }, last_message_float_time);
}

function _continuouslyFillActiveChatroomSpace () {
    var active_chatroom = $(".active-chatroom");
    var displaying = active_chatroom.css("display");
    var chatroom_id = active_chatroom.attr("chatroom-id");
    if (displaying !== "block" || chatroom_id == "") {
        return false;
    }
    fillChatroomSpace(chatroom_id);
}

function continuouslyFillActiveChatroomSpace () {
    setInterval(_continuouslyFillActiveChatroomSpace, (1000 * 3));
}

function addEventForChatroomListItems () {
    var chatroomListItems = document.querySelectorAll(".chatroom-list-item");

    for (var chatroomListItem of chatroomListItems) {
        var chatroom_id = chatroomListItem.getAttribute("chatroom-id");
        $(chatroomListItem).click(function () {
            changeActiveChatroom(chatroom_id);
            fillChatroomSpace(chatroom_id);
        });
    }
}

$(document).ready(function (){
	$("#chatroom_toggler").click(toggleChatroom);
    $("#list_chatrooms_btn").click(displayChatroomsList);
    $("#display_chatroom_details_btn").click(displayChatroomDetails);

    addEventForChatroomListItems();

	$("#send_chat").on("click", function (event) {
        event.preventDefault();

        var chatroom_id = $(".active-chatroom").attr("chatroom-id");

        var chatEntry = $("#chat_entry");
        if (chatEntry.val() == "") {
            alert("Message cannot be empty!");
            return false;
        }

        sendChat(chatEntry.val(), chatroom_id, function (data) {
            return true;
        });
    });

    getMyChatroomsList(function (chatrooms) {
        if (chatrooms.length == 0) {
            $(".chatrooms-list .chatroom-list-item-none").css({"display": "block"});
        }

        for (var chatroom of chatrooms) {
            addChatroomToDisplay(chatroom);
        }
        addEventForChatroomListItems();
        continuouslyFillActiveChatroomSpace();
    });
});

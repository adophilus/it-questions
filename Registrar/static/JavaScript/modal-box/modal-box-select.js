class ModalBoxSelect
{
	constructor (options) {
		this.visibility = false;
		this.closed = false;
		this.answer = undefined;
		this.modalOptions = new Object();
		this.modalOptions.title = "This is the title";
		this.modalOptions.body = "This is the body";
		this.modalOptions.type = "display";
		this.modalOptions.font = new Object();
		this.modalOptions.placeholder = "";
		this.modalOptions.font.title = $_("body").style.fontFamily + " lucida, arial";
		this.modalOptions.font.body = $_("body").style.fontFamily + " lucida, arial";
		this.modalOptions.callback = (data) => {};
		this.modalOptions.options = new Array();

		if (options) {
			for (var key in options) {
				this.modalOptions[key] = options[key];
			}
		}

		this.create();
		this.handleCommands();
		this.add();
	}

	create () {
		this.modalDiv = $$.createElement("div");
		this.modalDiv.setAttribute("class", "modal-select-container");

		this.modalHeader = $$.createElement("header");
		this.modalHeader.setAttribute("class", "modal-select-header");
		this.modalClose = $$.createElement("span");
		this.modalClose.setAttribute("class", "modal-select-close");

		this.modalBody = $$.createElement("div");
		this.modalBody.setAttribute("class", "modal-select-body");
		this.modalContent = $$.createElement("p");
		this.modalContent.setAttribute("class", "modal-select-content");

		this.modalFooter = $$.createElement("div");
		this.modalFooter.setAttribute("class", "modal-select-footer");
		this.modalSelect = $$.createElement("select");
		this.modalSelect.setAttribute("class", "modal-select-select");
		this.modalSelect.setAttribute("id", "modalSelect");

		this.buttonSpace = $$.createElement("div");
		this.buttonSpace.setAttribute("class", "modal-select-button-space");
		this.finishButton = $$.createElement("button");
		this.finishButton.setAttribute("class", "modal-select-finish-button");
		this.finishButton.innerHTML = "Ok";

		this.modalCover = $$.createElement("div");
		this.modalCover.setAttribute("class", "modal-select-cover");

		this.modalClose.innerHTML = "&times";
		this.modalBody.innerHTML = this.modalOptions.body;
	}

	add () {
		this.modalHeader.appendChild(this.modalClose);
		for (var opt of this.modalOptions.options) {
			var option = $$.createElement("option");
			option.innerHTML = opt;
			this.modalSelect.appendChild(option);
		}
		this.modalFooter.appendChild(this.modalSelect);
		this.modalFooter.appendChild(this.buttonSpace);
		this.buttonSpace.appendChild(this.finishButton);

		this.modalDiv.appendChild(this.modalHeader);
		this.modalDiv.appendChild(this.modalBody);
		this.modalDiv.appendChild(this.modalFooter);

		// this.modalBody.appendChild(this.modalContent);

		$_("body").appendChild(this.modalCover);
		$_("body").appendChild(this.modalDiv);
	}

	handleStyles () {
		// this.modalDiv.style.display = "none";
		// this.modalDiv.style.border = "3px solid blue";
		// this.modalDiv.style.borderRadius = "10px";
		// this.modalDiv.style.width = "50%";
		// this.modalDiv.style.position = "fixed";
		// this.modalDiv.style.userSelect = "none";
		// this.modalDiv.style.top = "30%";
		// this.modalDiv.style.left = "50%";
		// this.modalDiv.style.transform = "translate(-50%, -50%)";
		// this.modalDiv.style.boxShadow = "0px 8px 16px 8px #0d0d0d";
		// this.modalDiv.style.backgroundColor = "white";

		// this.modalHeader.style.fontSize = "30px";
		// this.modalHeader.style.fontWeight = "bolder";
		// this.modalHeader.style.padding = "10px";
		// this.modalHeader.style.backgroundColor = "white";
		// this.modalHeader.style.color = "black";
		// this.modalHeader.style.fontWeight = "900";
		// this.modalHeader.style.borderRadius = "10px 10px 0px 0px";
		// this.modalHeader.style.textAlign = "right";

		// this.modalBody.style.padding = "10px";
		// this.modalBody.style.fontSize = "25px";
		// this.modalBody.style.backgroundColor = "white";
		// this.modalBody.style.fontFamily = this.modalOptions.font.body;

		// this.modalContent.style.backgroundColor = "white";
		// this.modalContent.style.width = "100%";
		// this.modalContent.style.height = "100%";
		// this.modalContent.style.top = "0";
		// this.modalContent.style.left = "0";

		// this.modalFooter.style.backgroundColor = "white";
		// this.modalFooter.style.borderRadius = "0px 0px 8px 8px";
		// this.modalFooter.style.overflow = "auto";
		// this.modalFooter.style.textAlign = "center";

		// this.modalSelect.style.borderRadius = "10px";
		// this.modalSelect.style.padding = "10px";
		// this.modalSelect.style.width = "90%";
		// this.modalSelect.style.border = "2px solid blue";
		// this.modalSelect.style.fontSize = "20px";
		// this.modalSelect.style.fontWeight = "900";

		// this.buttonSpace.style.paddingTop = "20px";
		// this.buttonSpace.style.textAlign = "right";
		// this.buttonSpace.style.paddingRight = "10px";

		// this.finishButton.style.fontWeight = "bold";
		// this.finishButton.style.fontSize = "25px";
		// this.finishButton.style.backgroundColor = "white";
		// this.finishButton.style.border = "2px solid blue";
		// this.finishButton.style.borderRadius = "10px";
		// this.finishButton.style.transitionDuration = "0.4s";
		// this.finishButton.style.padding = "10px";
		// this.finishButton.style.paddingLeft = "20px";
		// this.finishButton.style.paddingRight = "20px";
		// this.finishButton.style.cursor = "pointer";

		// // this.modalClose.style.float = "right";
		// this.modalClose.style.cursor = "pointer";

		// this.modalCover.style.top = "0";
		// this.modalCover.style.left = "0";
		// this.modalCover.style.position = "fixed";
		// this.modalCover.style.display = "none";
		// this.modalCover.style.width = "100%";
		// this.modalCover.style.height = "100%";
		// this.modalCover.style.backgroundColor = "#333";
		// this.modalCover.style.opacity = "0.65";
	}

	handleFooter () {
		// this.modalBody.style.borderRadius = "0px 0px 8px 8px";
		// this.modalFooter.style.padding = "10px";
	}

	handleCommands () {
		var that = this;

		this.modalClose.onclick = function () {
			that.close();

			if (that.modalOptions.callback) {

				that.modalOptions.callback();

			}
		}

		this.modalCover.onclick = function () {
			that.close();

			if (that.modalOptions.callback) {

				that.modalOptions.callback();
				
			}
		}

		this.finishButton.onclick = function () {
			that.close();

			if (that.modalOptions.callback) {

				that.modalOptions.callback(that.modalSelect.value);
			
			}
		}

		// this.modalSelect.oninput = function (event) {
		// 	console.log(event.key);
		// 	if (event.key === "Enter") {
		// 		that.close();

		// 		if (that.modalOptions.callback) {

		// 			that.modalOptions.callback(that.modalSelect.value);
				
		// 		}
		// 	}
		// }

		if (this.closeButton) {

			this.closeButton.onclick = function () {

				that.close();

				if (that.modalOptions.callback) {

					that.modalOptions.callback();
				
				}
			}
		}

		if (this.noButton) {

			this.noButton.onclick = function () {

				that.close();

				that.answer = false;

				if (that.modalOptions.callback) {

					that.modalOptions.callback();
				
				}
			}
		}

		if (this.yesButton) {

			this.yesButton.onclick = function () {

				that.close();

				that.answer = true;

				if (that.modalOptions.callback) {

					that.modalOptions.callback();
				
				}
			}
		}
	}

	toggle () {
		if (this.visibility) {
			this.hide();
		}
		else {
			this.show();
		}
	}

	show () {
		this.modalDiv.style.display = "block";
		this.modalCover.style.display = "block";
		this.visibility = true;
		this.closed = false;
	}

	hide () {
		this.modalDiv.style.display = "none";
		this.modalCover.style.display = "none";
		this.visibility = false;
	}

	close () {
		this.hide();
		this.closed = true;
	}
}
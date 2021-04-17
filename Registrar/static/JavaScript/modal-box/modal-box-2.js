class ModalBox2
{
	constructor (options = {}) {
		this.visibility = false;
		this.closed = false;
		this.answer = undefined;
		this.modalOptions = new Object();
		this.modalOptions.title = "This is the title";
		this.modalOptions.body = "This is the body";
		this.modalOptions.type = "display";
		this.modalOptions.font = new Object();
		this.modalOptions.font.title = $_("body").style.fontFamily + " lucida, arial";
		this.modalOptions.font.body = $_("body").style.fontFamily + " lucida, arial";
		this.modalOptions.callback = function () {};

		if (options) {
			for (var key in options) {
				if (options[key]) {
					this.modalOptions[key] = options[key];
				}
			}
		}

		this.create();
		this.handleFooter();
		this.handleStyles();
		this.handleCommands();
		this.add();
	}

	callback () {}

	create () {
		this.modalDiv = $$.createElement("div");

		this.modalHeader = $$.createElement("header");
		this.modalClose = $$.createElement("span");

		this.modalBody = $$.createElement("div");
		this.modalContent = $$.createElement("p");

		this.modalFooter = $$.createElement("header");
		this.modalCover = $$.createElement("div");

		// this.modalClose.innerHTML = "&times";
		this.modalBody.innerHTML = this.modalOptions.body;
	}

	add () {
		this.modalHeader.appendChild(this.modalClose);

		this.modalDiv.appendChild(this.modalHeader);
		this.modalDiv.appendChild(this.modalBody);
		// this.modalDiv.appendChild(this.modalFooter);

		// this.modalBody.appendChild(this.modalContent);

		$_("body").appendChild(this.modalCover);
		$_("body").appendChild(this.modalDiv);
	}

	handleStyles () {
		this.modalDiv.style.display = "none";
		this.modalDiv.style.border = "3px solid #3468af";
		this.modalDiv.style.borderRadius = "10px";
		this.modalDiv.style.width = "50%";
		this.modalDiv.style.position = "fixed";
		this.modalDiv.style.userSelect = "none";
		this.modalDiv.style.top = "30%";
		this.modalDiv.style.left = "50%";
		this.modalDiv.style.transform = "translate(-50%, -50%)";
		this.modalDiv.style.boxShadow = "0px 8px 16px 8px #0d0d0d";
		this.modalDiv.style.backgroundColor = "white";

		// this.modalHeader.style.fontSize = "30px";
		this.modalHeader.style.fontSize = "inherit";
		this.modalHeader.style.fontWeight = "bolder";
		this.modalHeader.style.padding = "10px";
		this.modalHeader.style.backgroundColor = "white";
		this.modalHeader.style.color = "black";
		this.modalHeader.style.fontWeight = "900";
		this.modalHeader.style.borderRadius = "10px 10px 0px 0px";
		this.modalHeader.style.textAlign = "right";
		this.modalHeader.style.height = "0px";

		this.modalBody.style.padding = "10px";
		// this.modalBody.style.fontSize = "25px";
		this.modalBody.style.fontSize = "inherit";
		this.modalBody.style.backgroundColor = "white";
		// this.modalBody.style.fontFamily = this.modalOptions.font.body;

		this.modalContent.style.backgroundColor = "white";
		this.modalContent.style.width = "100%";
		this.modalContent.style.height = "100%";
		this.modalContent.style.top = "0";
		this.modalContent.style.left = "0";

		this.modalFooter.style.backgroundColor = "white";
		this.modalFooter.style.borderRadius = "0px 0px 8px 8px";
		this.modalFooter.style.padding = "10px";

		// this.modalClose.style.float = "right";
		this.modalClose.style.color = "black";
		this.modalClose.classList.add("flaticon-cancel");
		this.modalClose.style.cursor = "pointer";
		this.modalClose.style.fontWeight = "bolder";

		this.modalCover.style.top = "0";
		this.modalCover.style.left = "0";
		this.modalCover.style.position = "fixed";
		this.modalCover.style.display = "none";
		this.modalCover.style.width = "100%";
		this.modalCover.style.height = "100%";
		this.modalCover.style.backgroundColor = "#333";
		this.modalCover.style.opacity = "0.65";
	}

	handleFooter () {
		this.modalBody.style.borderRadius = "0px 0px 8px 8px";
		this.modalFooter.style.padding = "0px";
	}

	handleCommands () {
		var that = this;

		this.modalClose.onclick = function () {
			that.close(that);

			if (that.modalOptions.callback) {

				that.modalOptions.callback();

			}
		}

		this.modalClose.onmouseover = function () {
			this.style.color = "red";
		}

		this.modalClose.onmouseleave = function () {
			this.style.color = "black";
		}

		this.modalCover.onclick = function () {
			that.close(that);

			if (that.modalOptions.callback) {

				that.modalOptions.callback();

			}
		}

		if (this.closeButton) {

			this.closeButton.onclick = function () {

				that.close(that);

				if (that.modalOptions.callback) {

					that.modalOptions.callback();

				}
			}
		}

		if (this.noButton) {

			this.noButton.onclick = function () {

				that.close(that);

				that.answer = false;

				if (that.modalOptions.callback) {

					that.modalOptions.callback();

				}
			}
		}

		if (this.yesButton) {

			this.yesButton.onclick = function () {

				that.close(that);

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

	close (self) {
		self.hide();
		self.closed = true;
	}
}

class FlipSwitch
{
	constructor (options) {
		this.flipSwitchOptions = {
			"container": $$.createElement("div"),
			"label": $$.createElement("label"),
			"switch": $$.createElement("input"),
			"state": "on",
			"on_text": "On",
			"off_text": "Off"
		}
		this.states = {
			"true": "on",
			"false": "off"
		}
		for (var key in options) {
			this.flipSwitchOptions[key] = options[key];
		}

		this.assignAttributes();
		this.assignEvents();
		this.add();
		this.setState();
	}

	assignAttributes () {
		this.flipSwitchOptions.container.setAttribute("class", "flip-switch-container")
		this.flipSwitchOptions.label.setAttribute("class", "flip-switch-label");
		this.flipSwitchOptions.label.setAttribute("for", "flip-switch");
		this.flipSwitchOptions.switch.setAttribute("class", "sp switch flip-switch");
		this.flipSwitchOptions.switch.setAttribute("type", "checkbox");
		this.flipSwitchOptions.switch.setAttribute("id", "flip-switch");
		this.flipSwitchOptions.label.innerHTML = this.flipSwitchOptions[`${this.flipSwitchOptions.state}_text`];
	
	}

	setState (state) {
		this.flipSwitchOptions.state = state;
		if (this.flipSwitchOptions.state == this.states["true"]) {
			this.flipSwitchOptions.label.innerHTML = this.flipSwitchOptions.on_text;
			this.flipSwitchOptions.switch.checked = true;
		}
		else if (this.flipSwitchOptions.state == this.states["false"]) {
			this.flipSwitchOptions.label.innerHTML = this.flipSwitchOptions.off_text;
			this.flipSwitchOptions.switch.checked = false;
		}
	}

	setOnValue (value) {
		this.flipSwitchOptions.on_text = value;
		this.flipSwitchOptions.label.innerHTML = this.flipSwitchOptions["on_text"];
	}

	setOffValue (value) {
		this.flipSwitchOptions.off_text = value;
		this.flipSwitchOptions.label.innerHTML = this.flipSwitchOptions["off_text"];
	}

	changeState (state = null) {
		if (state === null) {
			state = !(state);
		}
		state = this.states[String(state)];
		this.setState(state);
	}

	assignEvents () {
		var that = this;
		this.flipSwitchOptions.switch.onchange = function (event) {
			if (event.target.checked) {
				that.flipSwitchOptions.state = "on";
			}
			else {
				that.flipSwitchOptions.state = "off";
			}

			that.setState();
		}
	}

	add () {
		this.flipSwitchOptions.container.appendChild(this.flipSwitchOptions.label);
		this.flipSwitchOptions.container.appendChild(this.flipSwitchOptions.switch);
	}

	create () {
		return this.flipSwitchOptions.container;
	}
}
window.customContextMenu = {}

class ContextMenu {
	constructor (contextMenuContents) {
		this.generator = new PrivateKeyGenerator();
		this.contextMenuContainer = $$.createElement("ul");
		this.contextMenuContainer.classList.add("context-menu-container");
		
		this.contextMenuId = this.generator.generate(3);
		this.contextMenuContainer.setAttribute("context-menu-id", this.contextMenuId);

		this.boundElements = new Array();

		for (var contextMenuItem of contextMenuContents) {
			this.add(contextMenuItem);
		}
	}

	handleContextMenuEvents (element) {
		var that = this;
		this.boundElements.push(element);
		
		element.onclick = function (event) {
			that.hide();
		}

		element.onkeydown = function (event) {
			if (event.keyCode == 27 || event.key == "Escape") {
				that.hide();
			}
		}

		element.oncontextmenu = function (event) {
			event.preventDefault();

			// that.show(event.offsetX, event.offsetY);
			that.show(event.x, event.y);
		}
	}

	create () {
		$_("body").appendChild(this.element());
		window.customContextMenu[this.contextMenuId] = this;
	}

	add (contextMenuItem) {
		this.contextMenuContainer.appendChild(contextMenuItem.element());
	}

	element () {
		return this.contextMenuContainer;
	}

	hide () {
		this.contextMenuContainer.classList.remove("context-menu-visible");
	}

	show (coords_x = 0, coords_y = 0) {
		this.contextMenuContainer.style.top = `${coords_y}px`;
		this.contextMenuContainer.style.left = `${coords_x}px`;
		this.contextMenuContainer.classList.add("context-menu-visible");
	}

	handleWindowContextMenuEvents () {
		window.onkeydown = function (event) {
			if (event.keyCode == 27 || event.key == "Escape") {
				ContextMenu.prototype.hideAll();
			}
		}

		window.onclick = function (event) {
			ContextMenu.prototype.hideAll();
		}
	}

	hideAll () {
		for (var contextMenu in window.customContextMenu) {
			window.customContextMenu[contextMenu].hide();
		}
	}
}

class ContextMenuItemCallback {
    constructor (onclickCallback = () => {}) {
	    this.callbacks = {
		    "click": onclickCallback
		}
	}

	onclick (callback) {
		if (!callback) {
			return this.callbacks.click;
		}
	}

	callback (callback_type, callback) {
		this.callbacks[callback_type] = callback;
	}

	bind (element) {
		for (var event in this.callbacks) {
			element["on" + event] = this.callbacks[event];
		}
	}
}

class ContextMenuItem {
	constructor (contextMenuItemIcon, contextMenuItemLabel, callbackManager = new ContextMenuItemCallback()) {
		this.contextMenuItemContainer = $$.createElement("li");
		this.contextMenuItemContainer.classList.add("context-menu-item");
		callbackManager.bind(this.contextMenuItemContainer);

		this.add(contextMenuItemIcon);
		this.add(contextMenuItemLabel);
	}

	add (contextMenuItem) {
		this.contextMenuItemContainer.appendChild(contextMenuItem.element());
	}

	element () {
		return this.contextMenuItemContainer;
	}
}

class ContextMenuItemIcon {
	constructor (icon_class = "") {
		this.contextMenuItemIcon = $$.createElement("span");
		this.contextMenuItemIcon.classList.add("context-menu-item-icon");
		(icon_class == "") ? "" : this.contextMenuItemIcon.classList.add(icon_class);
	}

	element () {
		return this.contextMenuItemIcon;
	}
}

class ContextMenuItemLabel {
	constructor (label_text, label_class = "") {
		this.contextMenuItemLabel = $$.createElement("span");
		this.contextMenuItemLabel.innerHTML = label_text;
		this.contextMenuItemLabel.classList.add("context-menu-item-label");
		(label_class == "") ? "" : this.contextMenuItemLabel.classList.add(label_class);
	}

	element () {
		return this.contextMenuItemLabel;
	}
}

class ContextMenuItemSeparator {
	constructor (separator_class = "") {
		this.contextMenuItemSeparator = $$.createElement("div");
		this.contextMenuItemSeparator.classList.add("context-menu-item-separator");
		(separator_class == "") ? "" : this.contextMenuItemSeparator.classList.add(separator_class);
	}

	element () {
		return this.contextMenuItemSeparator;
	}
}

// var eventCallback = new ContextMenuItemCallback(onclick = function (e) {
// 	console.log(e);
// 	window.poc = e;
// });

// var callback = new ContextMenuItemCallback(onclick = function () {
// 	console.log("Pasted + 1");
// });

// var refreshCallback = new ContextMenuItemCallback(onclick = function () {
// 	var elem = $$.createElement("a");
// 	elem.href = window.location.href;
// 	elem.click();
// });

// window.CMenu = new ContextMenu([
// 	new ContextMenuItem(new ContextMenuItemIcon("entypo-up"), new ContextMenuItemLabel("Event"), eventCallback),
// 	new ContextMenuItem(new ContextMenuItemIcon("fontawesome-cut"), new ContextMenuItemLabel("Cut")),
// 	new ContextMenuItem(new ContextMenuItemIcon("fontawesome-paste"), new ContextMenuItemLabel("Paste"), callback),
// 	new ContextMenuItemSeparator(),
// 	new ContextMenuItem(new ContextMenuItemIcon("fontawesome-refresh"), new ContextMenuItemLabel("Refresh"), refreshCallback),
// ]);

// var element = $_("body");
// window.CMenu.handleContextMenuEvents(element);
// window.CMenu.create();

// ContextMenu.prototype.handleWindowContextMenuEvents();

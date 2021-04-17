module.export = {
	"library": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",

	"generate": function (level = 4, separator = "-") {
		return this.generateKey(level);
	},

	"generateKey": function (level = 4, separator = "-") {
		var privateKey = "";

		for (var x = 0; x < level - 1; x++) {
			privateKey += this.generateKeyLevel();
			privateKey += separator;
		}

		privateKey += this.generateKeyLevel();

		return privateKey;
	},

	"generateKeyLevel": function () {
		var keyLevel = "";

		for (var x = 0; x < 4; x++) {
			var number = this.randomNumber(0, this.library.length - 1);

			var letter = this.library[number];

			keyLevel += letter;
		}

		return keyLevel;
	},

	"randomNumber": function (min, max) {
	    return Math.floor(Math.random() * (max - min + 1) + min);
	},
}

// var pkeygen = new PrivateKeyGenerator();
// var key = pkeygen.generateKey(4); // <- This is the key

// console.log(key);
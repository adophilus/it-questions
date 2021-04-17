class PrivateKeyGenerator
{
	constructor (library = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") {
		this.library = library;
	}

	generate (level = 4, separator = "-") {
		return this.generateKey(level);
	}

	generateKey (level = 4, separator = "-") {
		var privateKey = "";

		for (var x = 0; x < level - 1; x++) {
			privateKey += this.generateKeyLevel();
			privateKey += separator;
		}

		privateKey += this.generateKeyLevel();

		return privateKey;
	}

	generateKeyLevel () {
		var keyLevel = "";

		for (var x = 0; x < 4; x++) {
			var number = this.randomNumber(0, this.library.length - 1);
			
			var letter = this.library[number];

			keyLevel += letter;
		}

		return keyLevel;
	}

	randomNumber (min, max) {
	    return Math.floor(Math.random() * (max - min + 1) + min);
	}
}
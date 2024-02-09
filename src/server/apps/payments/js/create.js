const Hmac = require("./Hmac.js");

const args = process.argv;

result = Hmac.create(JSON.parse(args[2]), args[3])

console.log(result)

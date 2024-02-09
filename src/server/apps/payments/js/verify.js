const Hmac = require("./Hmac.js");

const args = process.argv;

result = Hmac.verify(JSON.parse(args[2]), args[3], args[4])

console.log(result)

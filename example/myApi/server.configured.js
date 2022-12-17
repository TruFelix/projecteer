const dotenv = require("dotenv");
const express = require("express");

dotenv.config();

const app = express();

app.get("/ping", (req, res) => {
	res.send("HELLO YOU!");
})

// even though this is not good practice it works:
// good practice would be to use .env file as a proxy
app.get(express.static("|SERVEROOT|"));

const port = process.env["PORT"];
const host = process.env["HOST"];
app.listen(port, host, () => {
	console.log(`running on http://${host}:${port}`);
})
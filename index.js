const express = require("express");
const app = express();

app.get("/", (res,req) => {
    res.
    res.render("index");
});

app.listen(process.env.PORT || 3000)
const express = require("express")
const app = express()

app.get("/", function (res,req) {
    res.render("index")
})

app.listen(process.env.PORT || 5000)
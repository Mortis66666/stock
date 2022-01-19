function makeRed (object) {
    object.style.borderColor = "red";
}

function addWarning (id, warning) {
    let element = document.getElementById(id);
    element.innerHTML = warning;
}

function removeWarning (id) {
    let element = document.getElementById(id);
    element.innerHTML = "";
}

function warn (object, warningId, reason) {
    makeRed(object);
    addWarning(warningId,reason)
}

function pass(object,warningId) {
    object.style.borderColor = "green";
    removeWarning(warningId);
}


function onInput () {
    let username = document.getElementById("username");
    let password = document.getElementById("password");
    let cpassword = document.getElementById("cpassword");

    // Username warning
    const uname = username.value;
    var id = "userWarning";

    if (uname.length < 4) {
        warn(username,id,"Username must have at least 4 characters");
    }
    else if (uname.length > 15) {
        warn(username,id,"Username cannot be more than 15 characters");
    }
}



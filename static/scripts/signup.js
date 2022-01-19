function makeRed (object) {
    object.style.borderColor = "red";
}

function addWarning (id, warning) {
    let element = document.getElementById(id);
    element.innerText = warning;
}

function removeWarning (id) {
    let element = document.getElementById(id);
    element.innerText = "";
}

function warn (object, warningId, reason) {
    makeRed(object);
    addWarning(warningId,reason)
}

function pass(object,warningId) {
    object.style.borderColor = "green";
    removeWarning(warningId);
}

function check (word) {
    const valids = "qwertyuiopasdfghjklzxcvbnm_1234567890";

    for (let char in word) {
        if (!valids.includes(word[char].toLowerCase())) {
            return false;
        }
    }
    return true;
}


function onInput () {
    let username = document.getElementById("username");
    let password = document.getElementById("password");
    let cpassword = document.getElementById("cpassword");

    // Username warning
    const uname = username.value;
    var id = "usernameWarning";

    if (uname.length == 0) {
        username.style.borderColor = null;
        removeWarning("usernameWarning");
    }
    else if (uname.length < 4) {
        warn(username,id,"Username must have at least 4 characters");
    }
    else if (uname.length > 15) {
        warn(username,id,"Username cannot be more than 15 characters");
    }
    else if (!check(uname)) {
        warn(username,id,"Username can only contain alphabets, numbers and \"_\"");
    }
    else {
        pass(username,id);
    }

    // Password warning
    const passwd = password.value;
    var id = "passwordWarning";

    if (passwd.length == 0) {
        password.style.borderColor = null;
        removeWarning("passwordWarning");
    }
    else if (passwd.length < 6) {
        warn(password,id,"Password must be atleast 6 characters");
    }
    else {
        pass(password,id)
    }

    // Confirm password warning
    const cpasswd = cpassword.value;
    var id = "cpasswordWarning";

    if (cpasswd.length == 0) {
        cpassword.style.borderColor = null;
        removeWarning("cpasswordeWarning");
    }
    else if (!cpasswd==passwd) {
        warn(cpassword,id,"The password must be the same");
    }
}

function onFocus () {
    pass;
}



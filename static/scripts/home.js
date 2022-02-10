const message = document.getElementById("message").value;

if (message) {
    alert(message);
};

setInterval(function () {
    $.getJSON("https://mortis666stocksimulator.herokuapp.com/stock_api?callback=?", function (data) { 
        $.each(data, function (key, value) { 
             
            var valueElement = document.getElementById("price"+key);
            var amountElement = document.getElementById("amount"+key);

            if (amountElement.innerText == 1) {
                valueElement = "💰" + value;
            }
        });
    });
}, 3000);

function increase (name) {

    const id = "amount"+name;
    const element = document.getElementById(id);
    const price = document.getElementById("price"+name);
    const amount = parseInt(element.innerText);

    element.innerText = amount + 1;
    price.innerText = "💰" + ((parseInt(price.innerText.replace("💰", "")) / amount) * (amount + 1));
};

function decrease (name) {

    const id = "amount"+name;
    const element = document.getElementById(id);
    const price = document.getElementById("price"+name);
    const amount = parseInt(element.innerText);

    if (amount > 1) {
        element.innerText = amount - 1;
        price.innerText = "💰" + ((parseInt(price.innerText.replace("💰", "")) / amount) * (amount - 1));
    }
};

function buy (stock_owner) {

    const amount = document.getElementById("amount"+stock_owner).innerText;
    window.location.href = `https://mortis666stocksimulator.herokuapp.com/buy?user=${stock_owner}&amount=${amount}&redirect=${window.location.href}`;
};

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
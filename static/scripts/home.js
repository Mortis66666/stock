const message = document.getElementById("message").value;

if (message) {
    alert(message);
};


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

setInterval(async () => {
    const settings = {
        "async": true,
        "crossDomain": true,
        "url": "https://mortis666stocksimulator.herokuapp.com/stock_api",
        "method": "GET",
        "headers": {
            "Accept": "*/*",
            "User-Agent": window.navigator.userAgent
        }
    };
      
    $.ajax(settings).done(response => {
        for (let [user, price] of Object.entries(response)) {
            let priceElement = document.getElementById("price"+user);
            let amountElement = document.getElementById("amount"+user);

            if (priceElement) {
                priceElement.innerHTML = "💰" + (price * +amountElement.innerHTML)
            }
        }
    });
}, 30000);

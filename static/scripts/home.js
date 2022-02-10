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

setInterval(() => {
    $.getJSON("https://mortis666stocksimulator.herokuapp.com/stock_api?callback=?", (data) => { 
        data.forEach((object) => {
                var stockName = object.username;
                var newPrice = object.stock_value;
                var priceElement = getElementById("price"+stockName);
                var amount = getElementById("amount"+stockName);

                console.log(`Stock name: ${stockName}`)
                console.log(`New price: ${newPrice}`)
                console.log(`Old price: ${priceElement.innerText}`)
                console.log(`Amount: ${amount.innerText}`)
                
                if (result) {
                    if (amount.innerText.trim() == 1) {
                        priceElement.innerText = "💰" + newPrice;
                    };
                };

            });
    });
}, 3000)
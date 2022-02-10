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

while (true) {
    $.getJSON("https://mortis666stocksimulator.herokuapp.com/stock_api", data,
        function (data, textStatus, jqXHR) {
            
            data.forEach(object => {
                
                var name = object.username;
                var price = object.stock_value;
                var result = getElementById("price"+name);
                var amount = getElementById("amount"+name);

                if (result) {
                    if (amount.innerText == 1) {
                        result.innerText = price;
                    };
                };

            });

        }
    );

    sleep(3000);
}
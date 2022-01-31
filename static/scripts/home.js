function increase (name) {

    const id = "amount"+name;
    const element = document.getElementById(id);
    const price = document.getElementById("price"+name);
    const amount = parseInt(element.innerText);

    element.innerText = amount + 1;
    price.innerText = "💰" + ((parseInt(price.innerText.slice(3)) / amount) * (amount + 1));
};

function decrease (name) {

    const id = "amount"+name;
    const element = document.getElementById(id);
    const price = document.getElementById("price"+name);
    const amount = parseInt(element.innerText);

    if (amount > 1) {
        element.innerText = amount - 1;
        price.innerText = "💰" + ((parseInt(price.innerText.slice(3)) / amount) * (amount - 1));
    }
};

function buy (stock_owner) {

    const amount = document.getElementById("amount"+stock_owner).innerText;
    window.location.href = `https://mortis666stocksimulator.herokuapp.com/buy?user=${stock_owner}&amount=${amount}`;
};
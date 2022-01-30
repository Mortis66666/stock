function increase (name) {

    const id = "amount"+name;
    const element = document.getElementById(id);
    const price = document.getElementById("price"+name)
    let amount = parseInt(element.value);

    element.value = amount + 1;
    price.innerText = (parseInt(price.innerText) / amount) * amount + 1;
};

function decrease (name) {

    const id = "amount"+name;
    const element = document.getElementById(id);
    let amount = parseInt(element.value);

    if (amount > 1) {
        element.value = amount + 1;
        price.innerText = (parseInt(price.innerText) / amount) * amount + 1;
    }
};
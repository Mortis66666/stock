function increase (name) {

    const id = "amount"+name;
    const element = document.getElementById(id)
    let amount = parseInt(element.innerText);

    element.innerText = amount + 1;

    // TODO handling some special cases: Negative number, amount more then stock amount
}
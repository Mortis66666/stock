const submit = document.getElementById("submit");

submit.addEventListener("mouseenter",(event)=>{
    submit.style.color = "gold";
})

submit.addEventListener("mouseleave",(event)=>{
    submit.style.color = "#00FF73";
})


const warning = document.getElementById("warning").value;

if (warning) {
    alert(warning);
}
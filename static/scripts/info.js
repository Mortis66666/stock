let owner = document.getElementById("name").innerHTML;
let data = JSON.parse(document.getElementById("history").innerHTML);

const labels = Array(data.length).fill("");

const config = {
    type: "line",
    data: {
        labels: Array(data.length).fill(""),
        datasets: [{
            label: `${owner}'s stock statistic`,
            backgroundColor: "rgb(0,255,115)",
            borderColor: "rgb(0,255,115)",
            data: data
        }]
    }
}

const chart = new Chart(
    document.getElementById("graph"),
    config
);
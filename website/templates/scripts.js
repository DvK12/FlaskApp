var canvasElement = document.getElementById("myChart");

var config = {
    type:"bar",
    data: {labels:  [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ], 
    datasets: [{label:"Net Benefit", 
    data: [3,12,3,2,4,5,6,8,9,-1,7,6],
    backgroundColor:["rgba(132, 217, 135, 0.55)"],
    borderColor: ["rgba(132, 217, 135, 1)"],
    borderWidth:1, 
}],
}
}

var myChart = new Chart(canvasElement, config)
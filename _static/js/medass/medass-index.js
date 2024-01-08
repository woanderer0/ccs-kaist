// JavaScript for the stopwatch
let stopwatchInterval;
let stopwatchTime;
let clockTime;

let recording = false;
const timeList = [];
const valueList = [];
const recordedData = [];

const stopwatch = document.getElementById("stopwatch");
const stopwatchValue = document.getElementById("stopwatchValue");
const startStopButton = document.getElementById("startStopButton");
const saveButton = document.getElementById("saveButton")
const csvInput = document.getElementById("csvInput")

function formatTime(milliseconds) {
    const seconds = milliseconds / 1000;
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = (seconds % 60).toFixed(2);
    return `${minutes}:${remainingSeconds}`;
}

startStopButton.addEventListener("click", () => {
    console.log(recording);
    if (recording) {
        const csvContent = recordedData.map(data => data.join(",")).join("\n");
        csvInput.value = encodeURI(csvContent);
        
        clearInterval(stopwatchInterval);
        startStopButton.innerText = "Start Recording";
        saveButton.disabled = false;
        
        var myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
        plotModal();
        myModal.show();
    } else {
        // Clear previous data
        timeList.length = 0; 
        valueList.length = 0;
        clockTime = new Date().getTime();
        
        // Start interval
        stopwatchInterval = setInterval(() => {
            stopwatchTime = new Date().getTime() - clockTime;
            let time = (stopwatchTime / 1000).toFixed(2);
            let value = slider.value;
            
            timeList.push(time);
            valueList.push(value);
            recordedData.push([time, value]);
        }, 10);
        
        startStopButton.innerText = "Stop Recording";
        saveButton.disabled = true;

        if (modalChart) {
            modalChart.destroy();
        }
    }
    recording = !recording;
});

// Plotting Module
const plotInterval = setInterval(() => {
    const Plotly = window.Plotly;
    let maxX = timeList[timeList.length - 1];
    let minX = maxX - 10;
    
    GRAPH = document.getElementById('plotting');
    
    Plotly.newPlot(GRAPH, [{x: timeList, y: valueList, type: 'scatter'}], { 
        xaxis: {
            title: "time",
            showline: false,
            range: [minX, maxX]
        },
        yaxis: {
            range: [0, 100]
        },
        margin: { t: 0 } 
    });
});

var modalChart;

function plotModal() {
    // Take input from html
    const Chart = window.Chart;
    
    color = Math.floor(Math.random() * 240);
    light = Math.floor(Math.random() * 80);
    
    GRAPH = document.getElementById('plotting-modal');
    
    modalChart = new Chart(GRAPH, {
        type: 'line',
        data: {
            labels: timeList,
            datasets: [{
                data: valueList,
                fill: false,
                borderColor: `hsl(${color}, 100%, ${light}%)`,
                tension: 0.1
            }]
        },
        options: {
            elements: {
                point: {
                    pointStyle: false
                },
            },
            plugins: {
                legend: {
                    display: false
                },
            },
            scales: {
                x: {
                    type: 'linear'
                },
                y: {
                    display: false,
                    min: -5,
                    max: 105
                },
            },
        },
        plugins: []
    });
}

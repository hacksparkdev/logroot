// script.js

const socket = io();
const logDisplay = document.getElementBy

Id('log-display');
const searchQuery = document.getElementById('search-query');
const searchResults = document.getElementById('search-results');

const ctx = document.getElementById('eventChart').getContext('2d');
const chartData = {
    labels: ['Error', 'Warning', 'Information'],
    datasets: [{
        label: '# of Events',
        data: [0, 0, 0],  // Placeholder data
        backgroundColor: ['rgba(255, 99, 132, 0.2)', 'rgba(255, 159, 64, 0.2)', 'rgba(54, 162, 235, 0.2)'],
        borderColor: ['rgba(255, 99, 132, 1)', 'rgba(255, 159, 64, 1)', 'rgba(54, 162, 235, 1)'],
        borderWidth: 1
    }]
};

const eventChart = new Chart(ctx, {
    type: 'bar',
    data: chartData,
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

socket.on('new_log', (log) => {
    const parsedLog = JSON.parse(log);
    logDisplay.innerHTML += `${JSON.stringify(parsedLog, null, 2)}\\n`;

    // Update chart based on log event type
    const eventType = parsedLog.EventType;
    if (eventType === 1) chartData.datasets[0].data[0]++;  // Error
    if (eventType === 2) chartData.datasets[0].data[1]++;  // Warning
    if (eventType === 3) chartData.datasets[0].data[2]++;  // Information
    eventChart.update();
});

document.getElementById('search-btn').addEventListener('click', () => {
    const query = searchQuery.value;
    socket.emit('search_logs', { message: query });
});

socket.on('search_results', (results) => {
    searchResults.innerHTML = results.map(r => JSON.stringify(r._source, null, 2)).join('\\n');
});


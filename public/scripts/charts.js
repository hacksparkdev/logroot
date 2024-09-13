// Function to fetch data from the server and render the chart
async function fetchDataAndRenderChart() {
    try {
        // Fetch data from your server
        const response = await fetch('/data');
        const data = await response.json();

        // Process data into format suitable for Chart.js
        const timestamps = data.map(item => new Date(item.timestamp).toLocaleDateString()); // Convert timestamp to readable date
        const results = data.map(item => item.result.length); // Example: Count the length of result string

        // Create chart using Chart.js
        const ctx = document.getElementById('myChart').getContext('2d');
        new Chart(ctx, {
            type: 'line', // Change type as needed (e.g., 'bar', 'pie', etc.)
            data: {
                labels: timestamps,
                datasets: [{
                    label: 'Result Length', // Label for the dataset
                    data: results,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    x: {
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Call the function to render the chart
fetchDataAndRenderChart();


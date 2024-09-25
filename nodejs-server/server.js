const express = require('express');
const bodyParser = require('body-parser');
const { Client } = require('@elastic/elasticsearch');

const app = express();
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({ extended: true }));

// Set up Elasticsearch client
const client = new Client({ node: 'http://10.10.20.107:9200' });

// Logs route (already in your code)
app.get('/logs', async (req, res) => {
    try {
        // Query Elasticsearch for logs
        const result = await client.search({
		index: 'winlogbeat-2024.09.25',  // Replace with your Elasticsearch index
            size: 20,            // Number of logs to display
            body: {
                query: {
                    match_all: {}  // Fetch all logs, you can customize this to match specific queries
                }
            }
        });

        // Pass logs to the EJS view
        res.render('logs', { logs: result.hits.hits });
    } catch (err) {
        console.error(err);
        res.status(500).send('Error fetching logs');
    }
});

// New Route: Fetch and display all alerts
app.get('/alerts', async (req, res) => {
    try {
        // Query Elasticsearch for alerts (replace 'alerts_index' with your actual index)
        const result = await client.search({
            index: 'alerts',  // Replace this with your alerts index
            size: 10,  // Adjust the number of alerts to display
            body: {
                query: {
                    match_all: {}  // Fetch all alerts, customize this as needed
                }
            }
        });

        // Render the alerts page with the data fetched from Elasticsearch
        res.render('alerts', { alerts: result.hits.hits });
    } catch (err) {
        console.error(err);
        res.status(500).send('Error fetching alerts');
    }
});

// New Route: Fetch and display a specific alert by ID
app.get('/alerts/:id', async (req, res) => {
    try {
        const alertId = req.params.id;

        // Fetch the specific alert by its ID
        const alert = await client.get({
            index: 'alerts',  // Replace 'alerts_index' with your actual alerts index
            id: alertId
        });

        // Render the alert details page
        res.render('alert_detail', { alert: alert._source });
    } catch (err) {
        console.error(err);
        res.status(500).send('Error fetching alert');
    }
});

app.listen(3000, () => {
    console.log('Server started on http://localhost:3000');
});


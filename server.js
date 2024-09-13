const express = require('express');
const { Client } = require('@elastic/elasticsearch');
const app = express();
const port = 3000;

// Initialize Elasticsearch client
const esClient = new Client({ node: 'http://10.10.20.107:9200' });

// Serve static files
app.use(express.static('public'));

// Endpoint to queue a Python module execution
app.post('/trigger-python-module', async (req, res) => {
    const { moduleName } = req.body;

    if (!moduleName) {
        return res.status(400).send('Module name is required');
    }

    try {
        // Create task in Elasticsearch
        const result = await esClient.index({
            index: 'python-tasks',
            document: {
                moduleName: moduleName,
                status: 'pending',
                created_at: new Date().toISOString()
            }
        });

        res.send(`Module ${moduleName} queued for execution with task ID: ${result._id}`);
    } catch (error) {
        console.error(`Error adding task to Elasticsearch: ${error.message}`);
        res.status(500).send('Error adding task');
    }
});

// Endpoint to fetch data for chart
app.get('/data', async (req, res) => {
    try {
        // Query Elasticsearch for completed tasks
        const result = await esClient.search({
            index: 'python-tasks',
            body: {
                query: {
                    match: { status: 'completed' }
                },
                sort: [{ created_at: { order: 'desc' } }]
            }
        });

        // Process the results
        const data = result.body.hits.hits.map(hit => ({
            timestamp: hit._source.created_at,
            moduleName: hit._source.moduleName,
            result: hit._source.result
        }));

        res.json(data);
    } catch (error) {
        console.error(`Error fetching data from Elasticsearch: ${error.message}`);
        res.status(500).send('Error fetching data');
    }
});

app.listen(port, () => {
    console.log(`Node.js server running on http://localhost:${port}`);
});

